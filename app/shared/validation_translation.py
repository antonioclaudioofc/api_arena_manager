ERROR_TRANSLATIONS = {
    "value_error.missing": "Campo obrigatório",
    "type_error.integer": "Deve ser um número inteiro",
    "type_error.float": "Deve ser um número",
    "type_error.bool": "Deve ser verdadeiro ou falso",
    "type_error.str": "Deve ser um texto",
    "value_error.email": "Email inválido",
    "value_error.any_str.min_length": "Texto muito curto",
    "value_error.any_str.max_length": "Texto muito longo",
    "value_error.number.not_gt": "Valor muito pequeno",
    "value_error.number.not_lt": "Valor muito grande",
}


def translate_error(error: dict):
    error_type = error.get("type")
    message = ERROR_TRANSLATIONS.get(error_type)

    if message:
        return message

    return "Valor inválido"
