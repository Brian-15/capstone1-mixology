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
        url: `${window.location.pathname}/bookmark`
    });

    $bookmark.attr('class', resp["data"]["CLASS"]);
}