
async function addLike(postId, target) {
    target.find("i").removeClass("fas fa-heart").addClass("fas fa-spinner")
    const response = await axios.post('/posts/like', { "post_id": postId })
    if (response.data.response) {
        target.removeClass("like-button").addClass("unlike-button has-text-danger").find("i").removeClass("fas fa-spinner").addClass("fas fa-heart")
    }
    else {
        target.find("i").removeClass("fas fa-spinner").addClass("fas fa-heart")
    }
}

async function removeLike(postId, target) {
    target.find("i").removeClass("fas fa-heart").addClass("fas fa-spinner")
    const response = await axios.post('/posts/unlike', { "post_id": postId })
    if (response.data.response) {
        target.removeClass("unlike-button has-text-danger").addClass("like-button").find("i").removeClass("fas fa-spinner").addClass("fas fa-heart")
    }
    else {
        target.find("i").removeClass("fas fa-spinner").addClass("fas fa-heart")
    }
}

async function deletePost(postId, parent) {
    const response = await axios.delete(`/posts/delete/${postId}`)
    if (response.data.response) {
        parent.remove()
    }
}

async function followUser(userId, target) {
    const response = await axios.post('/follow', { "follow_user_id": userId })
    if (response.data.response) {
        target.removeClass("follow-button").empty().addClass("unfollow-button is-outlined").html(
            `<span>
                Unfollow
            </span>
            <span class="icon">
                <i class="fas fa-minus"></i>
            </span>`
        )
    }
}

async function unfollowUser(userId, target) {
    const response = await axios.post('/unfollow', { "follow_user_id": userId })
    if (response.data.response) {
        target.removeClass("unfollow-button is-outlined").empty().addClass("follow-button").html(
            `<span>
                Follow
            </span>
            <span class="icon">
                <i class="fas fa-plus"></i>
            </span>`
        )
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
    else if (target.hasClass('follow-button')) {
        event.preventDefault()
        const UserId = target.attr('id')
        await followUser(UserId, target)
    }
    else if (target.parent().hasClass('follow-button')) {
        event.preventDefault()
        const UserId = target.parent().attr('id')
        await followUser(UserId, target.parent())
    }
    else if (target.hasClass('unfollow-button')) {
        event.preventDefault()
        const UserId = target.attr('id')
        await unfollowUser(UserId, target)
    }
    else if (target.parent().hasClass('unfollow-button')) {
        event.preventDefault()
        const UserId = target.parent().attr('id')
        await unfollowUser(UserId, target.parent())
    }
}
$(document).ready(function () {
    $('body').on('click', 'a', handleClick)
})

// Navbar toggle from bulma's documentation
$(document).ready(function() {

    // Check for click events on the navbar burger icon
    $(".navbar-burger").click(function() {
  
        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");
  
    });
  });