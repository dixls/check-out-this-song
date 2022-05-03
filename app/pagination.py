
def pagination(page_num=None):
    items_per_page = 5
    if page_num:
        first_post_index = page_num * items_per_page
        last_post_index = first_post_index+items_per_page
    else:
        first_post_index = 0
        last_post_index = items_per_page
    return {"first_post_index":first_post_index, "last_post_index":last_post_index, "items_per_page":items_per_page}