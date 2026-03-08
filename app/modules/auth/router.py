from html import escape

from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.modules.auth.dependencies import get_auth_service
from app.schemas.login import ForgotPasswordRequest, ResetPasswordRequest
from app.schemas.user import RequestUser, UserLogin
from app.schemas.token import Token
from starlette import status
from app.shared.schemas import MessageResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


def render_status_page(title: str, message: str, success: bool, status_code: int = 200):
    background = "#f4fff6" if success else "#fff5f5"
    border = "#2f9e44" if success else "#c92a2a"
    text = "#1f2937"

    return HTMLResponse(
        status_code=status_code,
        content=f"""
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <title>{escape(title)}</title>
            </head>
            <body style="margin:0;font-family:Segoe UI,Arial,sans-serif;background:{background};min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px;">
                <div style="max-width:560px;width:100%;background:#fff;border:1px solid {border};border-radius:12px;padding:24px;color:{text};box-shadow:0 8px 32px rgba(0,0,0,0.08)">
                    <h1 style="margin-top:0">{escape(title)}</h1>
                    <p style="margin-bottom:0;font-size:16px;line-height:1.5">{escape(message)}</p>
                </div>
            </body>
            </html>
            """
    )


def render_reset_password_form(token: str):
    safe_token = escape(token)

    return HTMLResponse(
        content=f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Recuperar senha</title>
        </head>
        <body style="margin:0;font-family:Segoe UI,Arial,sans-serif;background:#f8f9fa;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px;">
            <div style="max-width:560px;width:100%;background:#fff;border:1px solid #ced4da;border-radius:12px;padding:24px;box-shadow:0 8px 32px rgba(0,0,0,0.08)">
                <h1 style="margin-top:0;color:#1f2937">Definir nova senha</h1>
                <p style="margin-bottom:20px;color:#4b5563">Informe sua nova senha para concluir a recuperação.</p>
                <form method="post" action="/auth/reset-password-form">
                    <input type="hidden" name="token" value="{safe_token}" />
                    <label for="new_password" style="display:block;margin-bottom:8px;color:#111827">Nova senha</label>
                    <input id="new_password" name="new_password" type="password" minlength="6" required style="width:100%;padding:12px;border:1px solid #adb5bd;border-radius:8px;box-sizing:border-box;margin-bottom:16px" />
                    <button type="submit" style="background:#1971c2;color:#fff;border:none;border-radius:8px;padding:12px 16px;font-weight:600;cursor:pointer;width:100%">Redefinir senha</button>
                </form>
            </div>
        </body>
        </html>
        """
    )


@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def register(
    payload: RequestUser,
    auth_service=Depends(get_auth_service)
):
    auth_service.register(payload)

    return {
        "message": "Usuário criado com sucesso"
    }


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service=Depends(get_auth_service)
):
    payload = UserLogin(
        email=form_data.username,
        password=form_data.password
    )

    return auth_service.login(payload)


@router.get("/verify-email", response_class=HTMLResponse)
def verify_email(
    token: str,
    auth_service=Depends(get_auth_service)
):
    try:
        auth_service.verify_email(token)

        return render_status_page(
            title="E-mail verificado",
            message="Sua conta foi verificada com sucesso.",
            success=True,
        )
    except HTTPException as exc:
        return render_status_page(
            title="Falha na verificação",
            message=str(exc.detail),
            success=False,
            status_code=exc.status_code
        )


@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(
    payload: ForgotPasswordRequest,
    auth_service=Depends(get_auth_service)
):
    auth_service.forgot_password(payload.email)

    return {
        "message": "Enviado as instruções de recuperação para o e-mail."
    }


@router.post("/reset-password", response_model=MessageResponse)
def reset_password(
    payload: ResetPasswordRequest,
    auth_service=Depends(get_auth_service)
):
    auth_service.reset_password(payload.token, payload.new_password)

    return {
        "message": "Senha redefinida com sucesso"
    }


@router.get("/reset-password", response_class=HTMLResponse)
def reset_password_page(
    token: str,
    auth_service=Depends(get_auth_service)
):
    try:
        auth_service.validate_password_reset_token(token)
        return render_reset_password_form(token)
    except HTTPException as exc:
        return render_status_page(
            title="Link inválido",
            message=str(exc.detail),
            success=False,
            status_code=exc.status_code
        )


@router.post("/reset-password-form", response_class=HTMLResponse)
def reset_password_form(
    token: str = Form(...),
    new_password: str = Form(...),
    auth_service=Depends(get_auth_service)
):
    if len(new_password) < 6:
        return render_status_page(
            title="Senha inválida",
            message="A nova senha deve ter no mínimo 6 caracteres.",
            success=False,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    try:
        auth_service.reset_password(token, new_password)
        return render_status_page(
            title="Senha redefinida",
            message="Sua senha foi alterada com sucesso. Você já pode fazer login.",
            success=True,
        )
    except HTTPException as exc:
        return render_status_page(
            title="Não foi possível redefinir a senha",
            message=str(exc.detail),
            success=False,
            status_code=exc.status_code
        )
