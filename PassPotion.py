import secrets
import string
import math
import streamlit as st
import streamlit.components.v1 as components

# Password generation
def generate_password(length: int, include_upper: bool, include_numbers: bool, include_special: bool) -> str:
    lowercase = list(string.ascii_lowercase)
    uppercase = list(string.ascii_uppercase) if include_upper else []
    numbers = list(string.digits) if include_numbers else []
    special = list(string.punctuation) if include_special else []

    all_chars = lowercase + uppercase + numbers + special
    if not all_chars:
        raise ValueError("No character sets available to generate password.")

    password_chars = []
    # Guarantee at least one char of each selected type
    if uppercase:
        password_chars.append(secrets.choice(uppercase))
    if numbers:
        password_chars.append(secrets.choice(numbers))
    if special:
        password_chars.append(secrets.choice(special))

    remaining_length = length - len(password_chars)
    if remaining_length < 0:
        raise ValueError("Length is smaller than the number of required guaranteed characters.")

    password_chars += [secrets.choice(all_chars) for _ in range(remaining_length)]
    secrets.SystemRandom().shuffle(password_chars)
    return ''.join(password_chars)

# Entropy & strength calculation
def estimate_entropy(length: int, include_upper: bool, include_numbers: bool, include_special: bool) -> float:
    charset_size = len(string.ascii_lowercase)
    if include_upper:
        charset_size += len(string.ascii_uppercase)
    if include_numbers:
        charset_size += len(string.digits)
    if include_special:
        charset_size += len(string.punctuation)
    if charset_size <= 1:
        return 0.0
    return length * math.log2(charset_size)

def strength_label(entropy_bits: float) -> str:
    if entropy_bits < 28:
        return "Very weak"
    if entropy_bits < 36:
        return "Weak"
    if entropy_bits < 60:
        return "Moderate"
    if entropy_bits < 128:
        return "Strong"
    return "Very strong"

def strength_color(entropy_bits: float) -> str:
    """Return a hex color for the bar: red -> orange -> green gradient mapping."""
    # Normalize against a target 128 bits (cap at 128)
    pct = max(0.0, min(1.0, entropy_bits / 128.0))
    # red -> orange -> green gradient
    if pct < 0.5:
        # interpolate red (0xE53935) to orange (0xFB8C00)
        t = pct / 0.5
        r1, g1, b1 = (229, 57, 53)   # red
        r2, g2, b2 = (251, 140, 0)   # orange
    else:
        # interpolate orange to green (0x43A047)
        t = (pct - 0.5) / 0.5
        r1, g1, b1 = (251, 140, 0)   # orange
        r2, g2, b2 = (67, 160, 71)   # green

    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return f"rgb({r},{g},{b})"

# Streamlit UI
st.set_page_config(page_title="Pass Potion", page_icon="⚗️", layout="centered")

st.title("Pass Potion ⚗️")
st.write("Create strong, random passwords quickly. Customize your potion! "
         "see a color-coded strength bar, copy results, or download them as a file.")

# Sidebar controls
st.sidebar.header("Options")

length = st.sidebar.slider("Password length", min_value=8, max_value=256, value=16, step=1, help="Choose desired password length (minimum 8).")
include_upper = st.sidebar.checkbox("Include uppercase letters (A–Z)", value=True)
include_numbers = st.sidebar.checkbox("Include numbers (0–9)", value=True)
include_special = st.sidebar.checkbox("Include special characters (!@#$ etc.)", value=True)
count = st.sidebar.number_input("Number of passwords to generate", min_value=1, max_value=100, value=5, step=1)


st.sidebar.markdown("---")
st.sidebar.markdown("**Quick presets**")
if st.sidebar.button("Short (12)"):
    length = 12
if st.sidebar.button("Standard (16)"):
    length = 16
if st.sidebar.button("Long (32)"):
    length = 32

if not any([include_upper, include_numbers, include_special]):
    st.warning("No extra character types selected. Passwords will be lowercase letters only.")

# Generate
generate_pressed = st.button("Generate Password ⚗️")
passwords = []
if generate_pressed:
    try:
        for _ in range(count):
            passwords.append(generate_password(length, include_upper, include_numbers, include_special))
    except Exception as e:
        st.error(f"Error: {e}")

# Strength estimation + color-coded progress bar
entropy = estimate_entropy(length, include_upper, include_numbers, include_special)
label = strength_label(entropy)
color = strength_color(entropy)
pct = int(max(0.0, min(100.0, (entropy / 128.0) * 100)))

st.subheader("Strength estimate")
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"**Estimated entropy:** {entropy:.1f} bits — **{label}**")
    # Progress Bar Render to change color
    bar_html = f"""
    <div style="width:100%;background:#EEE;border-radius:8px;padding:3px;">
      <div style="
          width:{pct}%;
          background:{color};
          height:20px;
          border-radius:6px;
          transition: width 0.4s ease;">
      </div>
    </div>
    <div style="font-size:12px;color:#666;margin-top:6px;">Entropy: {entropy:.1f} bits — {pct}% of 128-bit target</div>
    """
    st.components.v1.html(bar_html, height=60)
with col2:
    # Small numeric badge
    st.metric("Progress to 128-bit", f"{pct}%")

st.caption("Aim for 60+ bits for general-purpose passwords; 128+ bits for extremely high security.")

# Display generated passwords, each with a copy button
st.subheader("Generated passwords")
if passwords:
    combined_text = "\n".join(passwords)
    for i, pw in enumerate(passwords, start=1):
        # show masked toggle and input
        mask_key = f"mask_{i}"
        masked = st.checkbox("Mask", value=True, key=mask_key)
        display_pw = "•" * len(pw) if masked else pw

        pw_col1, pw_col2, pw_col3 = st.columns([4, 1, 1])
        with pw_col1:
            st.text_input(f"Password {i}", value=display_pw, key=f"pw_display_{i}", disabled=True)
        with pw_col2:
            # copy button (JS)
            btn_id = f"copy_btn_{i}"
            html = f"""
            <button id="{btn_id}">Copy</button>
            <script>
            const btn = document.getElementById("{btn_id}");
            btn.onclick = () => {{
                navigator.clipboard.writeText({pw!r}).then(() => {{
                    const old = btn.innerText;
                    btn.innerText = "Copied!";
                    setTimeout(()=> btn.innerText = old, 1200);
                }});
            }};
            </script>
            """
            components.html(html, height=45)
        with pw_col3:
            st.download_button("Save", data=pw, file_name=f"password_{i}.txt", mime="text/plain")
    st.download_button("Download all passwords (.txt)", data=combined_text, file_name="passwords.txt", mime="text/plain")
else:
    st.info("Press **Generate Passwords** to create passwords.")

st.markdown("---")
st.markdown("**Tips**")
st.markdown(
    "- Use a password managers to store generated passwords securely.\n"
    "- Avoid re-using passwords across accounts.\n"
    "- For highest security choose longer lengths (24+) and include all character types."
)
