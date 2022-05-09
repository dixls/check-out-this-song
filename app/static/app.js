const $likeButton = $('#like-button')

async function addLike(postId, target) {
    const response = await axios.post('/posts/like', { "post_id": postId })
    if (response.data.response) {
        target.removeClass("like-button").addClass("unlike-button has-text-danger")
    }
}

async function removeLike(postId, target) {
    const response = await axios.post('/posts/unlike', { "post_id": postId })
    if (response.data.response) {
        target.removeClass("unlike-button has-text-danger").addClass("like-button")
    }
}

async function handleClick(event) {
    const target = $(event.target)
    if (target.hasClass('like-button')) {
        event.preventDefault()
        const postId = target.parent().parent().attr('id')
        await addLike(postId, target)
    }
    else if (target.hasClass('unlike-button')) {
        event.preventDefault()
        const postId = target.parent().parent().attr('id')
        await removeLike(postId, target)
    }
}

$('body').on('click', 'a', handleClick)