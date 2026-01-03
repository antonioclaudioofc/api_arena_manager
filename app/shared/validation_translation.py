ERROR_TRANSLATIONS = {
    "missing": "Campo obrigatório",

    "string_type": "Deve ser um texto",
    "int_parsing": "Deve ser um número inteiro",
    "float_parsing": "Deve ser um número",
    "bool_parsing": "Deve ser verdadeiro ou falso",

    "string_too_short": "Texto muito curto",
    "string_too_long": "Texto muito longo",

    "greater_than": "Valor muito pequeno",
    "less_than": "Valor muito grande",

    "enum": "Use apenas: admin ou client",

    "value_error.email": "Email inválido",
}


def translate_error(error: dict) -> str:
    error_type = error.get("type")

    if error_type in ERROR_TRANSLATIONS:
        return ERROR_TRANSLATIONS[error_type]

    if "enum" in str(error).lower():
        return "Valor inválido. Use apenas valores permitidos"

    return "Valor inválido"
