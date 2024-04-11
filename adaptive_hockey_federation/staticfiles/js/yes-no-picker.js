class YesNoPicker {
    constructor(selectActive) {
      this.selectActive = selectActive
      this._init()
    }

    _init() {
      this._populateSelect(this.selectActive, [["да", "True"], ["нет", "False"]], '----')
    }

    _populateSelect(selectElement, optionsArray, defaultValue) {
      selectElement.innerHTML = ''
      const defaultOption = document.createElement('option')
      defaultOption.value = ''
      defaultOption.selected = true
      defaultOption.textContent = defaultValue
      selectElement.appendChild(defaultOption)

      optionsArray.forEach(option => {
        const optionElement = document.createElement('option')
        optionElement.value = option[1]
        optionElement.textContent = option[0]
        selectElement.appendChild(optionElement)
      })
    }
  }
