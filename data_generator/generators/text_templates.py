# ==============================================================================
# Customer Support Operations Intelligence Platform - Ticket Text Templates
# ==============================================================================

import random

# Subject templates mapped by category
SUBJECT_TEMPLATES = {
    "Billing": [
        "Incorrect charge on my credit card",
        "Requesting refund for double billing",
        "Cannot update billing information",
        "Invoice request for last month",
        "Failed payment notification received",
        "Subscription renewal query",
        "Discrepancy in my billing statement",
        "How to apply coupon code to active plan?"
    ],
    "Technical": [
        "API returning 500 error code",
        "Dashboard widgets failing to load",
        "Websocket connection disconnects frequently",
        "Integration sync is failing",
        "CSV export returns empty file",
        "Platform is extremely slow today",
        "Error message when saving configuration",
        "Webhook notifications are not being sent"
    ],
    "Login/Access": [
        "Reset password link not received",
        "Locked out of my account due to too many attempts",
        "2FA verification code failing",
        "Cannot log in with SSO",
        "Permission denied error for team member",
        "How to transfer account ownership?",
        "Invite link expired for new user",
        "Account deactivated without warning"
    ],
    "Product Feedback": [
        "Feature request: bulk edit option",
        "Dark mode support request",
        "UX suggestions for dashboard page",
        "Requesting more customization in reports",
        "Feedback on new navigation bar layout",
        "Integrations list is missing a key tool",
        "Allow auto-export to Google Sheets",
        "Love the new calendar view!"
    ],
    "General": [
        "General inquiry regarding product capabilities",
        "How to schedule a demo for enterprise plan?",
        "Help with initial account setup",
        "Terms of service and privacy policy question",
        "Partner/affiliate program inquiry",
        "Holiday support hours question",
        "Is there a self-hosted option?",
        "Contact sales department"
    ]
}

# Description templates mapped by category and sentiment
# Sentiments: Positive, Neutral, Negative
DESCRIPTION_TEMPLATES = {
    "Billing": {
        "Positive": [
            "Hi, I noticed a duplicate charge on my invoice. Your support team has been great in the past so I know you will help me clear this up. Thank you!",
            "I wanted to update my billing info, and your UI is very smooth, but I wanted to make sure my credit card won't be charged twice during the switch. Appreciate your help!"
        ],
        "Neutral": [
            "Please find attached my request for a refund. I was charged twice for this month's billing cycle. Let me know when the refund is processed.",
            "I need my invoice for the month of June. It is not showing up in the billing settings panel. Please email a PDF version to me."
        ],
        "Negative": [
            "This is unacceptable. I was charged $99 twice on my card and I need this refunded immediately. Why does this keep happening? Very frustrated.",
            "Your payment system failed, and now my account is suspended even though I have paid. This is halting our business. Fix this right now!"
        ]
    },
    "Technical": {
        "Positive": [
            "Excellent tool overall, but I ran into a minor bug where the API endpoints are returning a 500 status on the test suite. Hope we can resolve it easily.",
            "The dashboard looks fantastic, but some widgets are not updating in real time. Can you let me know if there is a setting I need to adjust? Thanks!"
        ],
        "Neutral": [
            "We are encountering an issue where websocket connections disconnect every 15 minutes. Our network logs don't show local issues. Can you check on your end?",
            "I am trying to export our monthly tickets to a CSV file but the downloaded file contains no rows. Please advise on how to fix this."
        ],
        "Negative": [
            "Your API is constantly failing and breaking our integrations! This is a critical issue for us. We are losing data every hour this is down. Response needed urgently.",
            "The entire platform has been loading slow for the past three hours. Pages are timed out. I cannot do my work. This service reliability is terrible."
        ]
    },
    "Login/Access": {
        "Positive": [
            "Hi! I love your product but I'm locked out of my account because I forgot my password and the reset link hasn't arrived. I'd appreciate if you could reset it for me.",
            "Just setting up our SSO login and it is almost working. I just need you to verify the metadata XML format. Great documentation by the way!"
        ],
        "Neutral": [
            "I am locked out of my account after entering the wrong password. Please reset my attempts and send a temporary login link.",
            "My team member is getting a 'Permission Denied' error when trying to view the reports page, even though they are an admin. Please update their permissions."
        ],
        "Negative": [
            "I have requested a password reset five times and nothing has arrived in my spam or inbox. I am completely locked out of my dashboard. This is urgent and blocking my work!",
            "Your 2FA SMS code is not sending at all. I have been trying to log in for an hour. Why do you not support authentication apps? This is very frustrating."
        ]
    },
    "Product Feedback": {
        "Positive": [
            "I really love the clean interface of the tool! I'd like to suggest adding a dark mode option. It would make working late hours much more comfortable.",
            "The platform is already doing wonders for our team. We'd love it even more if we could auto-export reports directly to Google Sheets in the future. Keep up the great work!"
        ],
        "Neutral": [
            "We are currently reviewing features and would like to suggest a bulk-edit button for the issues list. This would help us manage tasks much faster.",
            "Could you add integration support for Slack notifications when tickets are escalated? This would fit nicely into our workflow."
        ],
        "Negative": [
            "The new navigation layout is really confusing. It takes twice as many clicks to find basic configuration pages. Please bring back the old sidebar design.",
            "I am highly disappointed that we cannot customize report graphs. The default widgets are too simple and don't meet our executive presentation needs."
        ]
    },
    "General": {
        "Positive": [
            "Hello, we are looking to roll out your tool to our support team and want to schedule a sales demo for 50+ licenses. Your platform looks like the perfect fit!",
            "I'm setting up our account and wanted to say how easy the onboarding guide was. Just writing to check if there are any specific guidelines for partner API access."
        ],
        "Neutral": [
            "Could you provide your holiday support schedule for the upcoming month? We want to ensure we align our workflows accordingly.",
            "Hello, is there a self-hosted/on-premise version of your software available, or is it strictly SaaS? Please let us know."
        ],
        "Negative": [
            "I tried to contact your sales team twice this week and no one has responded to my inquiries. If this is how you treat prospective clients, we will look elsewhere.",
            "I have some questions about how you handle data privacy and compliance. Your online documentation is vague and I need a direct answers before our security audit."
        ]
    }
}

def generate_text(category, sentiment):
    """
    Generates a subject and description based on the category and sentiment.
    """
    subjects = SUBJECT_TEMPLATES.get(category, SUBJECT_TEMPLATES["General"])
    desc_by_sentiment = DESCRIPTION_TEMPLATES.get(category, DESCRIPTION_TEMPLATES["General"])
    descriptions = desc_by_sentiment.get(sentiment, desc_by_sentiment["Neutral"])
    
    subject = random.choice(subjects)
    description = random.choice(descriptions)
    return subject, description
