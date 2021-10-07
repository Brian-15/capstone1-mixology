$deleteForm = $('#delete-user');

$deleteForm.submit(handleDeleteForm)

async function handleDeleteForm() {
    await axios.delete(window.location.pathname);
}