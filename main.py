from fastapi import FastAPI, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Set up Jinja2 template rendering
templates = Jinja2Templates(directory="templates")


conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about.html", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/projects.html", response_class=HTMLResponse)
async def projects(request: Request):
    return templates.TemplateResponse("projects.html", {"request": request})


@app.get("/contact.html", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


@app.get("/resume.html", response_class=HTMLResponse)
async def resume(request: Request):
    return templates.TemplateResponse("resume.html", {"request": request})


@app.get("/contactInfo.html", response_class=HTMLResponse)
async def contact_info(request: Request):
    return templates.TemplateResponse("contactInfo.html", {"request": request})


@app.post("/send-email/", response_class=HTMLResponse)
async def send_email(email: str = Form(...), message: str = Form(...)):
    print(email, message)
    # Email content
    msg = MessageSchema(
        subject="New Contact Form Submission",
        recipients=['salisbury.jeffery@gmail.com'],  # Replace with your email
        body=f"Email: {email}\n\nMessage: {message}",
        subtype="plain"
    )

    # # Send email
    fm = FastMail(conf)
    await fm.send_message(msg)

    # Return success message for HTMX to update UI
    return '<p class="text-green-600">Email sent successfully! I will get back to you soon.</p>'


# Serve static files (if needed for CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
