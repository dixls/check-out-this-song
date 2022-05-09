
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

async function deletePost(postId, parent) {
    const response = await axios.delete(`/posts/delete/${postId}`)
    if (response.data.response) {
        parent.remove()
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
    else if (target.hasClass('delete-button')) {
        event.preventDefault()
        const parent = target.parent().parent()
        const postId = parent.attr('id')
        await deletePost(postId, parent)
    }
}
$( document ).ready(function() {
    $('body').on('click', 'a', handleClick)
})