def generate_links(groups: tuple[str]):
    answer = "\n".join([f'→ <a href="{group[1]}">{group[0]}</a>' for group in groups])
    return answer
