import argparse
import json
import re


def parse_config(input_path):
    """Функция для парсинга конфигурационного файла."""
    try:
        with open(input_path, 'r') as file:
            content = file.read()

        # Удаление комментариев
        content = remove_comments(content)

        # Преобразование содержимого в JSON
        config_data = parse_content(content)

        return config_data
    except Exception as e:
        print(f"Ошибка при чтении или обработке файла: {e}")
        return None



import re


def remove_comments(input_content):
    # Удаление многострочных комментариев
    input_content = re.sub(r'/\+.*?\+/', '', input_content, flags=re.DOTALL)

    # Удаление однострочных комментариев (начинающихся с "::")
    input_content = re.sub(r'::.*', '', input_content)

    # Удаление комментариев, начинающихся с "#"
    input_content = re.sub(r'#.*', '', input_content)

    # Разделяем текст на строки и очищаем пустые строки
    lines = input_content.splitlines()
    cleaned_lines = [line for line in lines if line.strip() != '']

    # Объединяем строки обратно
    return '\n'.join(cleaned_lines)




def evaluate_postfix(expression, context):
    stack = []
    tokens = expression.split()
    for token in tokens:
        if token.isdigit():
            stack.append(int(token))
        elif token in context:
            # Используем значение переменной из контекста
            stack.append(context[token])
        elif token == '+':
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)
        elif token == '-':
            b = stack.pop()
            a = stack.pop()
            stack.append(a - b)
        elif token == '*':
            b = stack.pop()
            a = stack.pop()
            stack.append(a * b)
        elif token == 'sort()':
            array = stack.pop()
            if isinstance(array, list):
                stack.append(sorted(array))
            else:
                raise ValueError(f"Ожидался массив для sort(), а найдено: {array}")
        else:
            raise ValueError(f"Неизвестный токен: {token}")
    return stack.pop() if stack else None



def parse_content(content):
    config_data = {}
    lines = content.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("let "):
            match = re.match(r"let ([a-zA-Z_]+) = (.+)", line)
            if match:
                name, value = match.groups()
                if value.startswith("${") and value.endswith("}"):
                    # Убираем ${ и } и передаем в функцию для вычисления
                    value = evaluate_postfix(value[2:-1].strip(), config_data)
                else:
                    value = parse_value(value)
                config_data[name] = value
            else:
                raise ValueError(f"Ошибка синтаксиса: {line}")
    return config_data



def parse_value(value):
    value = value.strip()
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]  # Строка
    elif value.startswith("array(") and value.endswith(")"):
        items = value[6:-1].split(",")
        # Попробуем удалить кавычки вокруг каждого элемента, если они есть
        parsed_items = []
        for item in items:
            item = item.strip()
            if item.startswith("'") and item.endswith("'"):
                parsed_items.append(item[1:-1])  # Убираем кавычки
            elif item.isdigit():
                parsed_items.append(int(item))  # Преобразуем в число
            else:
                parsed_items.append(item)
        return parsed_items
    elif value.isdigit():
        return int(value)  # Число
    else:
        raise ValueError(f"Неизвестное значение: {value}")





def main():
    parser = argparse.ArgumentParser(description="Конфигурационный парсер для учебного языка.")
    parser.add_argument('--input', type=str, required=True, help="Путь к входному файлу")
    parser.add_argument('--output', type=str, required=True, help="Путь к выходному файлу (JSON)")

    args = parser.parse_args()

    # Парсинг входного файла
    config_data = parse_config(args.input)

    if config_data is not None:
        # Сохранение результата в файл
        with open(args.output, 'w') as outfile:
            json.dump(config_data, outfile, indent=4)
        print(f"Конфигурация успешно сохранена в {args.output}")


if __name__ == "__main__":
    main()
