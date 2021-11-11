import pandas as pd
from flask import Blueprint, flash, redirect, render_template, request, url_for, abort, Markup
from flask_login import current_user, login_required

from remainder import db
from remainder.main.utils import get_scalers
from remainder.models import Sleep
from remainder.records.forms import SleepRecordForm, UploadForm
from remainder.records.utils import try_parse, encode_daily_record_graph

records_bp = Blueprint('records', __name__)


@records_bp.route('/records/add', methods=('GET', 'POST'))
@login_required
def add():
    form = SleepRecordForm()
    if form.validate_on_submit():
        sleep_record = Sleep(up=form.up.data, to_bed=form.to_bed.data, user=current_user)
        db.session.add(sleep_record)
        db.session.commit()
        flash('A new records has been created!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('records/add.html', form=form,
                           title='Add', legend='New Record')


@records_bp.route('/records/<int:sleep_id>/update', methods=('GET', 'POST'))
@login_required
def update(sleep_id):
    sleep_record = Sleep.query.get_or_404(int(sleep_id))
    if sleep_record.user != current_user:
        abort(403)

    form = SleepRecordForm()
    if form.validate_on_submit():
        sleep_record.up = form.up.data
        sleep_record.to_bed = form.to_bed.data
        db.session.commit()
        the_day = sleep_record.up.date()
        flash(f'Record for {the_day} has been updated!', 'success')
        return redirect(url_for('main.dashboard'))

    elif request.method == 'GET':
        form.up.data = sleep_record.up
        form.to_bed.data = sleep_record.to_bed

    return render_template('records/add.html', form=form,
                           title='Update', legend='Update Record')


@records_bp.route('/records/<int:sleep_id>/delete', methods=['POST'])
@login_required
def delete(sleep_id):
    sleep_record = Sleep.query.get_or_404(sleep_id)
    if sleep_record.user != current_user:
        abort(403)
    db.session.delete(sleep_record)
    db.session.commit()
    the_day = sleep_record.up.date()
    flash(f'Record for {the_day} has been deleted!', 'success')

    return redirect(url_for('main.dashboard'))


@records_bp.route('/records/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        # extract filename and data from the file
        filename = form.csv.data.filename
        csv_data = form.csv.data
        df_data = pd.read_csv(csv_data)

        # process data
        parsed = df_data.applymap(try_parse)
        cleaned = parsed.dropna()
        
        data_to_add = []
        for i in range(len(cleaned)):
            datum = cleaned.iloc[i, :].to_dict()
            data_to_add.append(datum)

        records_to_add = [Sleep(up=d['up'], to_bed=d['to_bed'], user=current_user) for d in data_to_add]

        # import data into database
        db.session().add_all(records_to_add)
        db.session().commit()

        flash(f'Out of {len(parsed)} records imported from {filename}, {len(cleaned)} records are valid.\n', 'info')
        flash(f'{len(cleaned)} new records has been created!', 'success')

        return redirect(url_for('main.dashboard'))

    return render_template('records/upload.html', form=form,
                           legend='Add from CSV', title='Upload')


@records_bp.route('/records/graph')
@login_required
def graph():
    daily_records = list(Sleep.query.filter_by(user=current_user).
        order_by(Sleep.up.desc()).limit(14))

    base_dts, up_deltas, bed_deltas, sleep_sec = get_scalers(daily_records)

    up = [up.total_seconds() for up in up_deltas]
    bed = [bed.total_seconds() for bed in bed_deltas]

    plot_url = encode_daily_record_graph(
        date=base_dts,
        sleep=sleep_sec,
        up=up,
        bed=bed
        )

    graph_html_string = Markup(
        f'<img src="data:image/png;base64,{plot_url}" width: 800px; height: 800px>'
        )

    return render_template('/records/graph.html', title='Graph',
                            graph_html_string=graph_html_string)
