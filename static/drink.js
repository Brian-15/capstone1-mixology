/// Script for drink.html template

$bookmark = $('i');

$bookmark.click(handleBookmark);

/// Event Handler for bookmark icon click.  
async function handleBookmark() {
    let method;
    if ($bookmark.hasClass('bi-bookmark-fill')) {
        method = "delete";
    }
    else {
        method = "post";
    }

    const resp = await axios({
        method: method,
        url: `/bookmark`,
        data: {'id': window.location.pathname.split('/').at(-1)}
    });

    if (resp["data"]["STATUS"] == "OK") {
        $bookmark.attr('class', resp["data"]["CLASS"]);
    }
}