$bookmarksList = $('#bookmarks');
$deleteForm = $('#delete-user');

$deleteForm.submit(handleDeleteForm);
$bookmarksList.click(handleDeleteBookmark);

async function handleDeleteForm() {
    await axios.delete(window.location.pathname);
}

async function handleDeleteBookmark(evt) {
    if ($(evt.target).attr('class') == 'btn btn-danger') {
        await axios({
            method: 'delete',
            url: `/bookmark`,
            data: {'id': $(evt.target).attr('id')}
        });

        $(evt.target).parent().remove()
    }
}