import os

BASE_DIR = os.getcwd()

# Create project-level folders
project_dirs = ["templates", "static", "media"]
for folder in project_dirs:
    os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)

# Define your full app structure
apps = {
    "accounts": {
        "py_files": ["forms.py", "signals.py", "urls.py"],
        "html_files": ["login.html", "register.html", "profile_created.html", "role_selector.html"]
    },
    "dashboard": {
        "html_files": ["base_dashboard.html", "unauthorized.html"]
    },
    "homepage": {
        "html_files": ["index.html", "discover_talents.html", "emergency_aid.html", "sponsor_donate.html",
                       "become_agent.html", "become_talent.html", "login_register.html", "about.html", "updates.html"]
    },
    "wallet": {
        "py_files": ["forms.py"],
        "html_files": ["deposit.html", "withdraw.html", "transfer.html", "wallet.html"]
    },
    "crypto": {
        "html_files": ["pay.html", "success.html", "failure.html", "crypto_payment.html"]
    },
    "agents": {
        "html_files": ["dashboard.html", "registered_users.html", "collateral.html", "comission_status.html",
                       "p2p_request.html", "confirm_payment.html"]
    },
    "p2p_payments": {
        "py_files": ["forms.py"],
        "html_files": ["request_payment.html", "choose_agent.html", "user_pending.html", "thank_you.html"]
    },
    "employers": {
        "html_files": ["dashboard.html", "search_talent.html", "contact_talent.html", "interview_talent.html", "pay_access.html"]
    },
    "sponsor_donate": {
        "html_files": ["dashboard.html", "sponsor_case.html", "donation_records.html", "search_case.html", "contact_admin.html"]
    },
    "emergencies": {
        "html_files": ["dashboard.html", "register_emergency.html", "aid_request_list.html", "public_profiles.html",
                       "view_profile.html", "edit_profiles.html"]
    },
    "talents": {
        "html_files": ["dashboard.html", "upload.html", "my_creatives.html", "edit_profile.html", "shared_base.html"]
    },
    "artists": {
        "html_files": ["dashboard.html", "upload_creative.html", "view_portfolio.html"]
    },
    "coders": {
        "html_files": ["dashboard.html", "upload_project.html", "repo_links.html"]
    },
    "footballers": {
        "html_files": ["dashboard.html", "upload_video.html", "match_slots.html"]
    },
    "influencers": {
        "html_files": ["dashboard.html", "audience.html", "campaigns.html"]
    },
    "filmmakers": {
        "html_files": ["dashboard.html", "upload_film.html", "trailers.html"]
    },
    "profiles": {
        "html_files": ["view_profile.html", "edit_profile.html", "visibility_toggle.html"]
    },
    "messaging": {
        "html_files": ["inbox.html", "thread.html", "compose.html", "newmessage.html", "chat.html"]
    },
    "admin_panel": {
        "html_files": ["dashboard.html", "user_management.html", "transactions.html", "payment_management.html",
                       "profile_status.html", "public_status.html", "role_overview.html", "p2p_management.html",
                       "view_p2p_transactions.html", "verify_agent.html"]
    },
    "notifications": {
        "html_files": ["all_notifications.html", "mark_as_read.html", "enable_notification.html"]
    },
    "audit_logs": {
        "py_files": ["middleware.py"],
        "html_files": ["logs.html"]
    },
    "moderation": {
        "html_files": ["review_uploads.html", "review_profiles.html"]
    },
    "search": {
        "py_files": ["forms.py"],
        "html_files": ["search_results.html"]
    },
    "reviews": {
        "html_files": ["submit_review.html", "view_reviews.html"]
    },
    "referrals": {
        "html_files": ["referral_dashboard.html"]
    },
    "settingspanel": {
        "html_files": ["global_settings.html"]
    },
    "support_tickets": {
        "html_files": ["submit_ticket.html", "my_tickets.html", "admin_ticket_panel.html"]
    },
    "blog": {
        "html_files": ["blog_list.html", "blog_details.html"]
    },
    "api": {
        "py_files": ["serializers.py"]
    },
    "info": {
        "html_files": ["info.html"]
    },
    "broadcast": {
        "html_files": ["broadcast.html"]
    },
    "chat": {
        "py_files": ["consumers.py", "routing.py"],
        "html_files": ["chat.html", "static.css"]
    },
    "analytic": {
        "html_files": ["analytics.html"]
    },
    "emails": {
        "html_files": ["emails.html"]
    },
    "regions": {
        "html_files": ["africa.html", "america.html", "asia.html", "europe.html", "australia.html"]
    }
}

def make_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_file(path, content=""):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(content)

# Loop through apps
for app, contents in apps.items():
    app_dir = os.path.join(BASE_DIR, app)

    # Only create app if it doesn't exist
    if not os.path.exists(app_dir):
        os.system(f'python manage.py startapp {app}')

    # Ensure urls.py is always present
    contents.setdefault("py_files", [])
    if "urls.py" not in contents["py_files"]:
        contents["py_files"].append("urls.py")

    # Create .py files
    for py_file in contents["py_files"]:
        file_path = os.path.join(app_dir, py_file)
        if py_file == "urls.py":
            create_file(file_path, "from django.urls import path\n\nurlpatterns = []\n")
        else:
            create_file(file_path)

    # Create templates
    if contents.get("html_files"):
        templates_dir = os.path.join(app_dir, "templates", app)
        make_dirs(templates_dir)
        for html in contents["html_files"]:
            create_file(os.path.join(templates_dir, html), f"<!-- {html} -->")

    # Add static/ directory
    static_dir = os.path.join(app_dir, "static", app)
    make_dirs(static_dir)

    print(f"✅ App created: {app} — Don't forget to add it to settings.py > INSTALLED_APPS")

print("🎉 All apps, template folders, static directories, and starter files created successfully.")
