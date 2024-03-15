$('#add-achievement-form').submit(function (e) {
    e.preventDefault();

    var text = $('#achievement-text').val();
    addAchievement(text);
});

function addAchievement(text) {
    $.ajax({
        type: 'POST',
        url: '/achievements/new',
        data: {'achievement-text': text},
        success: function (response) {
            $('#achievements-section').append(response.new_achievement_html);
            updateAchievements();
        },
        error: function (error) {
            console.error(error);
        }
    });
}

function updateAchievements() {
    location.reload();
}