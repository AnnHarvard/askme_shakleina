function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


const init = () => {
    const questions = document.querySelectorAll('.question')
    const answers = document.querySelectorAll('.answer')


    for (const question of questions) {

        const likeButton = question.querySelector('.like-button')
        const likeCounter = question.querySelector('.like-counter')
        const questionId = question.dataset.questionId
        const likeIcon = likeButton.querySelector('.like-icon')
        // const filledHeart = likeIcon.dataset.filledHeart
        // const emptyHeart = likeIcon.dataset.emptyHeart

        likeButton.addEventListener('click', () => {
            const request = new Request(`/questions/${questionId}/like_question/`, {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            })

            fetch(request)
                .then((response) => response.json())
                .then((data) => {
                    likeCounter.innerHTML = data.likes_count;
                    if (likeIcon.src.includes('heart-fill.svg')) {
                        likeIcon.src = '/static/img/heart.svg';
                    } else {
                        likeIcon.src = '/static/img/heart-fill.svg';
                    }
                });
        })
    }

    for (const answer of answers) {

        const likeButton = answer.querySelector('.like-button')
        const likeCounter = answer.querySelector('.like-counter')
        const answerId = answer.dataset.answerId
        const questionId = answer.dataset.questionId;
        const likeIcon = likeButton.querySelector('.like-icon')


        likeButton.addEventListener('click', () => {
            const request = new Request(`/answers/${answerId}/like_answer/`, {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            })

            fetch(request)
                .then((response) => response.json())
                .then((data) => {
                    likeCounter.innerHTML = data.likes_count;
                    if (likeIcon.src.includes('heart-fill.svg')) {
                        likeIcon.src = '/static/img/heart.svg';
                    } else {
                        likeIcon.src = '/static/img/heart-fill.svg';
                    }
                });
        })

        const correctAnswerCheckbox = answer.querySelector('.correct-answer-checkbox');
        if (correctAnswerCheckbox) {
            correctAnswerCheckbox.addEventListener('change', () => {
                const isCorrect = correctAnswerCheckbox.checked;
                const request = new Request(`/questions/${questionId}/answers/${answerId}/mark_correct/?is_correct=${isCorrect}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                });

                fetch(request)
                    .then((response) => response.json())
                    .then((data) => {
                        if (data.status === 'success') {
                            console.log('Answer marked as correct.');
                        } else {
                            console.error('Invalid response data:', data);
                        }
                    })
                    .catch((error) => console.error('Error:', error));
            });
        }
    }
}

init()