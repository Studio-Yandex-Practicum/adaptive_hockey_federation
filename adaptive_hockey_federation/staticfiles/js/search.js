const searchFieldElement = document.getElementById("search_form_input")
const datePickerContainer = document.getElementById("date-picker")
const activePickerContainer = document.getElementById("active-picker-select")
const genderPickerContainer = document.getElementById("gender-picker-select")
const disciplineNamePickerContainer = document.getElementById("discipline-name-picker-select")

const searchColumnSelect = document.getElementById("search_column")
const searchColumnOptions = document.querySelectorAll("#search_column option")

const submitButton = document.getElementById("search_button")

const datePicker = new DatePicker(
    document.getElementById('date-picker-year'),
    document.getElementById('date-picker-month'),
    document.getElementById('date-picker-day'),
)

const activePicker = new OptionsPicker(
    document.getElementById("active-picker-select"),
    [["да", "true"], ["нет", "false"]],
)

const genderPicker = new OptionsPicker(
    document.getElementById("gender-picker-select"),
    [["женский", "женский"], ["мужской", "мужской"]],
)

const disciplinePicker = new DisciplineNamePicker(
    document.getElementById("discipline-name-picker-select"),
)

function toggleInputDisplay() {
    const selectedOption = searchColumnOptions[searchColumnSelect.selectedIndex]
    const searchKey = selectedOption.id

    const searchDateKeys = ["search_date", "search_date_end", "search_birthday"]

    if (searchDateKeys.includes(searchKey)) {
        searchFieldElement.style.display = "none"
        datePickerContainer.style.display = "flex"
        activePickerContainer.style.display = "none"
        genderPickerContainer.style.display = "none"
        disciplineNamePickerContainer.style.display = "none"

    } else if (searchKey === "search_is_active") {
        searchFieldElement.style.display = "none"
        datePickerContainer.style.display = "none"
        activePickerContainer.style.display = "flex"
        genderPickerContainer.style.display = "none"
        disciplineNamePickerContainer.style.display = "none"

    } else if (searchKey === "search_gender") {
        searchFieldElement.style.display = "none"
        datePickerContainer.style.display = "none"
        activePickerContainer.style.display = "none"
        genderPickerContainer.style.display = "flex"
        disciplineNamePickerContainer.style.display = "none"

    } else if (searchKey === "search_discipline_name"){
        searchFieldElement.style.display = "none"
        datePickerContainer.style.display = "none"
        activePickerContainer.style.display = "none"
        genderPickerContainer.style.display = "none"
        disciplineNamePickerContainer.style.display = "flex"
    }
     else {
        searchFieldElement.style.display = "flex"
        datePickerContainer.style.display = "none"
        activePickerContainer.style.display = "none"
        genderPickerContainer.style.display = "none"
        disciplineNamePickerContainer.style.display = "none"
    }
}
searchColumnSelect.addEventListener("change", toggleInputDisplay)
toggleInputDisplay()
