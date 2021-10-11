/// Script for drinks.html template

let page = 1;


$drinksList = $('#drinks-list');
$searchForm = $('form');
$nameField = $('#name');
$categoryField = $('#category');
$ingredientField = $('#ingredient')
$clearBtn = $('#clear-btn');
$prevPageBtns = $('.previous');
$nextPageBtns = $('.next');

populateDrinks(page);

$prevPageBtns.click(() => {
    page = page - 1;
    populateDrinks(page, $searchForm.serializeArray());
});

$nextPageBtns.click(() => {
    page = page + 1;
    populateDrinks(page, $searchForm.serializeArray());
});

$searchForm.on('submit', handleSearchForm);

/// Clears SearchForm fields upon button click
$clearBtn.click(() => {
    $nameField.val('');
    $categoryField.val('0');
    $ingredientField.val('0');
});

async function populateDrinks(page, formData) {

    const data = {"page": page};

    if (formData) {
        $.each(formData, (index, field) => {
            data[field.name] = field.value;
        });
        console.log(data);
    }

    const resp = await axios.post(`/drinks`, data);

    if (resp.data["next"]) {
        $nextPageBtns.show();
    }
    else {
        $nextPageBtns.hide();
    }

    if (resp.data["prev"]) {
        $prevPageBtns.show();
    }
    else {
        $prevPageBtns.hide();
    }

    drinkData = resp.data["drinks"];

    $drinksList.html('');

    for (let drink of drinkData) {
        $drinksList.append(
            $('<tr>').attr('id', drink['id']).append([
                $('<td>').append(
                    $('<img>').attr({
                        'src': drink.image_url,
                        'width': '200px',
                        'class': 'mx-auto d-inline rounded img-thumbnail',
                        'alt': ''
                    })
                ),
                $('<td>').attr('class', 'align-middle').append(
                    $('<a>').attr({
                        'href': `/drinks/${drink['id']}`,
                        'class': 'display-5 d-inline text-decoration-none text-wrap'
                    }).text(drink['name'])
                ),
                $('<td>').attr('class', 'align-middle').append(
                    $('<h1>').attr('class', 'd-inline text-right')
                    .append(
                        $('<span>').attr({
                            'id': drink["category_id"],
                            'class': 'tag-pill rounded-pill bg-primary text-light px-3',
                        }).text(drink["category"])
                    )
                )
            ])
        );
    }
}

/// Event Handler function for handling AJAX requests via Axios to the server, fetches drink data, and replaces drink list on DOM
function handleSearchForm(evt) {

    evt.preventDefault();

    page = 1;

    populateDrinks(1, $searchForm.serializeArray());
}