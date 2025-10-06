import os
import gradio as gr
from supabase import create_client, Client

# --- read secrets from your HF Space (you already added them) ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_ANON_KEY in Space secrets.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def do_signup(email: str, password: str):
    try:
        supabase.auth.sign_up({"email": email.strip(), "password": password})
        return "✅ Sign-up requested. Now go to the Sign-in tab."
    except Exception as e:
        return f"❌ Sign-up error: {e}"

def do_signin(email: str, password: str):
    try:
        res = supabase.auth.sign_in_with_password({"email": email.strip(), "password": password})
        token = getattr(getattr(res, "session", None), "access_token", None)
        return token or "❌ Sign-in failed (no token)."
    except Exception as e:
        return f"❌ Sign-in error: {e}"

def whoami(token: str):
    token = (token or "").strip()
    if not token:
        return {"error": "No token. Sign in first."}
    try:
        out = supabase.auth.get_user(token)
        user = getattr(out, "user", None)
        if user:
            return {"id": user.id, "email": user.email, "aud": user.aud}
        return {"error": "Invalid token."}
    except Exception as e:
        return {"error": str(e)}

with gr.Blocks(title="Supabase Auth Demo") as demo:
    gr.Markdown("# Supabase Auth Demo\nCreate an account, sign in, then check your identity.")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Sign up")
            su_email = gr.Textbox(label="Email")
            su_pass = gr.Textbox(label="Password", type="password")
            su_out = gr.Textbox(label="Result", interactive=False)
            gr.Button("Create account").click(do_signup, [su_email, su_pass], su_out)

        with gr.Column():
            gr.Markdown("### Sign in")
            si_email = gr.Textbox(label="Email")
            si_pass = gr.Textbox(label="Password", type="password")
            token_box = gr.Textbox(label="JWT (stored after sign-in)", interactive=False)
            gr.Button("Sign in").click(do_signin, [si_email, si_pass], token_box)

            gr.Markdown("### Who am I?")
            who_out = gr.JSON(label="User info (from Supabase)")
            gr.Button("Call whoami").click(whoami, [token_box], who_out)

if __name__ == "__main__":
    demo.launch()
