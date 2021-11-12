import os
import datetime

from flask import Blueprint, flash, render_template, Markup, Response, request, redirect, url_for
from flask_login import current_user, login_required

from remainder.models import Sleep
from remainder.main.utils import (
    hour_min, get_scalers, avg_delta,
    estimate_remaining_of_today, config_pie, encode_pie_chart,
    sql_query_to_csv
)
from remainder.main.forms import ContactForm
from remainder.users.utils import send_email


main_bp = Blueprint('main', __name__)


@main_bp.route('/main/')
@login_required
def dashboard():
    daily_records = list(Sleep.query.filter_by(user=current_user).
                         order_by(Sleep.up.desc()))

    page = request.args.get('page', 1, type=int)

    records_pagination = Sleep.query.filter_by(user=current_user).\
        order_by(Sleep.up.desc()).paginate(page=page, per_page=5)

    # Summary part and Remaining Time part
    # Default information: NO RECORD
    dashboard = {
        'avg_up': 'NO RECORD',
        'avg_bed': 'NO RECORD',
        'avg_sleep': 'NO RECORD',
        'bed_time': 'NO RECORD',
        'remaining': 'NO RECORD'
    }

    # If there's been no daily_records, use Default information in the view
    if len(daily_records) == 0:
        return render_template('/dashboard.html',
                               records_pagination=records_pagination,
                               dashboard=dashboard)

    else:
        # Summary part
        _, up_deltas, bed_deltas, sleep_sec = get_scalers(daily_records)

        avg_up = avg_delta(up_deltas)
        avg_bed = avg_delta(bed_deltas)
        avg_sleep = sum(sleep_sec) / len(sleep_sec)

        dashboard['avg_up'] = avg_up[7:12]
        dashboard['avg_bed'] = avg_bed[7:12]
        dashboard['avg_sleep'] = '{0[0]} hrs {0[1]} mins'.format(hour_min(int(avg_sleep)))

        # Remaining Time part
        timezone = current_user.timezone
        up_today_dt = daily_records[0].up
        bed_time, remaining = estimate_remaining_of_today(avg_sleep, up_today_dt, timezone)
        dashboard['bed_time'] = str(bed_time)[5:-3]
        dashboard['remaining'] = '{0[0]} hrs {0[1]} mins'.format(hour_min(remaining))

        if remaining < 0:
            flash("Need a new records to refresh Remaining Time!", 'alert')
            dashboard['remaining'] = '[Record for Today must be added]'

        # Pie-chart for Remaining Time
        plot_url = encode_pie_chart(config_pie(remaining, up_today_dt, timezone))

        pie_html_string = Markup(
            f'<img src="data:image/png;base64,{plot_url}" width: 360px; height: 288px>'
        )

        return render_template('/dashboard.html',
                               records_pagination=records_pagination,
                               dashboard=dashboard,
                               pie_html_string=pie_html_string)


@main_bp.route('/main/download')
@login_required
def download():
    daily_records = list(Sleep.query.filter_by(user=current_user).order_by(Sleep.up.desc()))
    csv = sql_query_to_csv(daily_records, columns_to_exclude=['user_id', 'id', '_sa_instance_state', 'created_at'])
    date = datetime.date.today().strftime('%Y%m%d')
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 f"attachment; filename=record_{date}.csv"})


@main_bp.route('/main/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        admin_email = os.environ.get('EMAIL_REMAINDER')

        config_forward = {
            'subject': f'Message from User ({form.firstname.data})',
            'bodyText': f"""{form.firstname.data} {form.lastname.data} ({form.email.data}) wrote\n\nMessage:\n{form.message.data}""",
            'fromAddress': admin_email,
            'toAddress': admin_email
        }
        send_email(config_forward)

        config_thank = {
            'subject': f"We've got your message!",
            'bodyText': f"""Dear {form.firstname.data},\n\n
Thank you for contacting us! We've received your message and will get back to you within 48 hours.\n
Cheers,\nRemainder Admin\nREMAINDER\nhttps://remainder-app.herokuapp.com/""",
            'fromAddress': admin_email,
            'toAddress': form.email.data
        }
        send_email(config_thank)
        flash("Thank you!\nWe've received your message and will get back to you within 48 hours.", 'success')
        return redirect(url_for('main.contact'))
    return render_template('contact.html', title='Contact Us', form=form)
