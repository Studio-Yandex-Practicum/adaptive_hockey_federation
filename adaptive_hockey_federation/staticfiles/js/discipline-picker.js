class DisciplineNamePicker {
  constructor(selectActive, optionsArray) {
    this.selectActive = selectActive;
    this.optionsArray = optionsArray;
    this._init()
  }

  _init() {
    this._getDiscipline().then(data => {
      const disciplineNames = data.map(discipline => discipline.name);
      this._populateSelect(this.selectActive, disciplineNames, '----');
    });
  }

  _getDiscipline() {
    return new Promise((resolve, reject) => {
      $.ajax({
        url: '/ajax/filter-discipline-search/',
        type: 'get',
        success: function(data) {
          resolve(data);
        },
        error: function(error) {
          reject(error);
        }
      });
    });
  }

  _populateSelect(selectElement, optionsArray, defaultValue) {
    selectElement.innerHTML = '';
    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.selected = true;
    defaultOption.textContent = defaultValue;
    selectElement.appendChild(defaultOption);

    optionsArray.forEach(option => {
      const optionElement = document.createElement('option');
      optionElement.value = option;
      optionElement.textContent = option;
      selectElement.appendChild(optionElement);
    });
  }
}
