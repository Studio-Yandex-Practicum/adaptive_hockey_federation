class OptionsPicker {
  constructor(selectActive, optionsArray) {
    this.selectActive = selectActive;
    this.optionsArray = optionsArray;
    this._populateSelect(this.selectActive, this.optionsArray, '----');
  }

  clearOptions() {
    this.optionsArray = [];
    this._populateSelect(this.selectActive, this.optionsArray, '----');
  }

  addOption(value, text) {
    this.optionsArray.push([text, value]);
    this._populateSelect(this.selectActive, this.optionsArray, '----');
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
      optionElement.value = option[1];
      optionElement.textContent = option[0];
      selectElement.appendChild(optionElement);
    });
  }
}
