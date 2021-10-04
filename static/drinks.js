/// Script for drinks.html template

$drinksList = $('#drinks-list');
$searchForm = $('form');
$searchForm.on('submit', handleForm);
$nameField = $('#name');
$categoryField = $('#category');
$ingredientField = $('#ingredient')
$clearBtn = $('#clear-btn');

/// Clears SearchForm fields upon button click
$clearBtn.click(evt => {
    $nameField.val('');
    $categoryField.val('0');
    $ingredientField.val('0');
});

/// Event Handler function for handling AJAX requests via Axios to the server, fetches drink data, and replaces drink list on DOM
async function handleForm(evt) {

    evt.preventDefault();

    formData = $searchForm.serializeArray();

    const resp = await axios.post('/drinks', formData);

    drinkData = resp.data;

    console.log("form submitted");

    $drinksList.html('');

    for (let drink of drinkData) {
        $drinksList.append(
            $('<div>').attr({
                'id': drink['id'],
                'class': 'list-group-item list-group-item-action'
            }).append([
                $('<img>').attr({
                    'src': drink.image_url,
                    'width': '200px',
                    'class': 'mx-auto d-inline rounded img-thumbnail',
                    'alt': ''
                }),
                $('<a>').attr({
                    'href': `/drinks/${drink['id']}`,
                    'class': 'display-5 d-inline text-decoration-none'
                }).text(drink['name']),
                $('<span>').attr({
                    'id': drink["category_id"],
                    'class': 'badge-pill badge-info',
                }).text(drink["category"])
            ])
        );
    }
}
