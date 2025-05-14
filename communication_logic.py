# communication_logic.py

import json
from datetime import datetime

TRANSLATIONS = {
    "en": {
        "profile_transition_notification": "Your profile has been updated to {new_profile_id} from {old_profile_id} due to {reason}. This may affect your financial plan recommendations.",
        "risk_score_update_notification": "Your risk score has been updated to {new_score} ({new_rating}). Investment suitability may have changed.",
        "economic_slowdown_alert": "Economic indicators suggest a potential slowdown (e.g., GDP growth at {gdp_growth}%). We recommend reviewing your plan with your MFD. Consider {fund_suggestion} for stability.",
        "plan_locked_notification": "Your financial plan (Version {plan_version}) created on {date} is now active and locked for 3 years to ensure stability.",
        "annual_health_check_reminder": "It's time for your annual financial plan health check. Please consult your MFD to review and update your plan.",
        "default_greeting": "Hello {investor_name}",
        "consent_prompt_sms_email": "Do you consent to receive important financial plan updates and notifications via SMS and Email? (Reply YES/NO)"
    },
    "hi": {
        "profile_transition_notification": "आपकी प्रोफ़ाइल {reason} के कारण {old_profile_id} से {new_profile_id} में अपडेट की गई है। यह आपकी वित्तीय योजना की सिफारिशों को प्रभावित कर सकता है।",
        "risk_score_update_notification": "आपका जोखिम स्कोर {new_score} ({new_rating}) पर अपडेट किया गया है। निवेश उपयुक्तता बदल सकती है।",
        "economic_slowdown_alert": "आर्थिक संकेतक संभावित मंदी का सुझाव देते हैं (उदाहरण के लिए, जीडीपी वृद्धि {gdp_growth}% पर)। हम आपके एमएफडी के साथ अपनी योजना की समीक्षा करने की सलाह देते हैं। स्थिरता के लिए {fund_suggestion} पर विचार करें।",
        "plan_locked_notification": "आपकी वित्तीय योजना (संस्करण {plan_version}) जो {date} को बनाई गई थी, अब सक्रिय है और स्थिरता सुनिश्चित करने के लिए 3 साल के लिए लॉक कर दी गई है।",
        "annual_health_check_reminder": "यह आपकी वार्षिक वित्तीय योजना स्वास्थ्य जांच का समय है। कृपया अपनी योजना की समीक्षा और अद्यतन करने के लिए अपने एमएफडी से परामर्श करें।",
        "default_greeting": "नमस्ते {investor_name}",
        "consent_prompt_sms_email": "क्या आप एसएमएस और ईमेल के माध्यम से महत्वपूर्ण वित्तीय योजना अपडेट और सूचनाएं प्राप्त करने के लिए सहमति देते हैं? (YES/NO में उत्तर दें)"
    }
}

def get_translated_message(message_key: str, language: str = "en", **kwargs) -> str:
    """Retrieves a translated message string, formatting it with provided arguments."""
    lang_pack = TRANSLATIONS.get(language, TRANSLATIONS["en"])
    message_template = lang_pack.get(message_key, f"Message key not found: {message_key}")
    try:
        return message_template.format(**kwargs)
    except KeyError as e:
        # Corrected print statement and ensure return is on a new line
        print(f"Warning: Missing placeholder {e} for message key '{message_key}' in language '{language}'.")
        return message_template

def generate_profile_transition_notification(old_profile_id: str, new_profile_id: str, reason: str, language: str = "en") -> dict:
    message = get_translated_message(
        "profile_transition_notification", language,
        old_profile_id=old_profile_id, new_profile_id=new_profile_id, reason=reason
    )
    return {"type": "profile_transition", "language": language, "content": message, "timestamp": datetime.now().isoformat()}

def generate_risk_score_update_notification(new_score: int, new_rating: str, language: str = "en") -> dict:
    message = get_translated_message(
        "risk_score_update_notification", language,
        new_score=new_score, new_rating=new_rating
    )
    return {"type": "risk_score_update", "language": language, "content": message, "timestamp": datetime.now().isoformat()}

def generate_economic_slowdown_alert(gdp_growth: float, fund_suggestion: str, language: str = "en") -> dict:
    message = get_translated_message(
        "economic_slowdown_alert", language,
        gdp_growth=gdp_growth, fund_suggestion=fund_suggestion
    )
    return {"type": "economic_alert", "language": language, "content": message, "timestamp": datetime.now().isoformat()}

def record_communication_consent(investor_id: str, sms_allowed: bool, email_allowed: bool) -> dict:
    """Conceptually records communication consent."""
    return {
        "action": "communication_consent_update",
        "investor_id": investor_id,
        "sms_allowed": sms_allowed,
        "email_allowed": email_allowed,
        "timestamp": datetime.now().isoformat()
    }

def send_app_notification(investor_id: str, notification_payload: dict):
    """Placeholder for sending an in-app notification."""
    print(f"APP NOTIFICATION for Investor ID {investor_id}:")
    print(f"  Type: {notification_payload.get('type')}")
    print(f"  Language: {notification_payload.get('language')}")
    print(f"  Content: {notification_payload.get('content')}")
    print(f"  Timestamp: {notification_payload.get('timestamp')}")
    return {"status": "success", "channel": "app", "message_logged": True}

def send_sms_notification(investor_id: str, mobile_number: str, notification_payload: dict):
    """Placeholder for sending an SMS. Logs the attempt and content."""
    print(f"SMS NOTIFICATION to {mobile_number} (Investor ID {investor_id}):")
    print(f"  Language: {notification_payload.get('language')}")
    print(f"  Content: {notification_payload.get('content')}")
    return {"status": "simulated_success", "channel": "sms", "message_logged": True, "note": "Actual SMS sending requires paid gateway."}

def send_email_notification(investor_id: str, email_address: str, subject: str, notification_payload: dict):
    """Placeholder for sending an Email. Logs the attempt and content."""
    print(f"EMAIL NOTIFICATION to {email_address} (Investor ID {investor_id}):")
    print(f"  Subject: {subject}")
    print(f"  Language: {notification_payload.get('language')}")
    print(f"  Content (body): {notification_payload.get('content')}")
    return {"status": "simulated_success", "channel": "email", "message_logged": True, "note": "Actual email sending requires SMTP setup/service."}

if __name__ == "__main__":
    print("--- Test Communication Logic ---")

    greeting_en = get_translated_message("default_greeting", "en", investor_name="John Doe")
    greeting_hi = get_translated_message("default_greeting", "hi", investor_name="जॉन डो")
    print(f"English Greeting: {greeting_en}")
    print(f"Hindi Greeting: {greeting_hi}")

    profile_notif_en = generate_profile_transition_notification("W1", "W2", "income increase", "en")
    profile_notif_hi = generate_profile_transition_notification("W1", "W2", "आय में वृद्धि", "hi")
    print("\nProfile Transition Notification (EN):", json.dumps(profile_notif_en, indent=2, ensure_ascii=False))
    print("Profile Transition Notification (HI):", json.dumps(profile_notif_hi, indent=2, ensure_ascii=False))

    risk_notif_en = generate_risk_score_update_notification(75, "High (Growth-Oriented)", "en")
    print("\nRisk Score Update Notification (EN):", json.dumps(risk_notif_en, indent=2))

    econ_alert_en = generate_economic_slowdown_alert(gdp_growth=3.8, fund_suggestion="Value Funds", language="en")
    econ_alert_hi = generate_economic_slowdown_alert(gdp_growth=3.8, fund_suggestion="वैल्यू फंड", language="hi")
    print("\nEconomic Slowdown Alert (EN):", json.dumps(econ_alert_en, indent=2))
    print("Economic Slowdown Alert (HI):", json.dumps(econ_alert_hi, indent=2, ensure_ascii=False))

    consent_log_entry = record_communication_consent("INV-20250101-0001", sms_allowed=True, email_allowed=False)
    print("\nConsent Log Entry:", json.dumps(consent_log_entry, indent=2))

    print("\nTesting Notification Sending Stubs:")
    send_app_notification("INV-TEST-001", profile_notif_en)
    send_sms_notification("INV-TEST-001", "9999988888", profile_notif_hi)
    send_email_notification("INV-TEST-001", "test@example.com", "Financial Plan Update", risk_notif_en)

    missing_placeholder_msg = get_translated_message("profile_transition_notification", "en", new_profile_id="W3")
    print(f"\nMessage with missing placeholder: {missing_placeholder_msg}")

