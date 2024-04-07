class DatePicker {
  constructor(yearSelect, monthSelect, daySelect) {
    this.yearSelect = yearSelect
    this.monthSelect = monthSelect
    this.daySelect = daySelect
    this._init()
  }

  _init() {
    this._populateSelect(this.yearSelect, this._getYears(), 'гггг')
    this._populateSelect(this.monthSelect, this._getMonths(), 'мм')
    this._updateDays()

    this.yearSelect.addEventListener('change', () => this._updateDays())
    this.monthSelect.addEventListener('change', () => this._updateDays())
  }

  _getYears() {
    const currentYear = new Date().getFullYear()
    return Array.from({ length: currentYear - 1999 }, (_, i) => currentYear - i)
  }

  _getMonths() {
    return Array.from({ length: 12 }, (_, i) => (i + 1).toString().padStart(2, '0'))
  }

  _populateSelect(selectElement, optionsArray, defaultValue) {
    selectElement.innerHTML = ''
    const defaultOption = document.createElement('option')
    defaultOption.value = ''
    defaultOption.disabled = true
    defaultOption.selected = true
    defaultOption.textContent = defaultValue
    selectElement.appendChild(defaultOption)

    optionsArray.forEach(option => {
      const optionElement = document.createElement('option')
      optionElement.value = option
      optionElement.textContent = option
      selectElement.appendChild(optionElement)
    })
  }

  _updateDays() {
    const year = parseInt(this.yearSelect.value)
    const month = parseInt(this.monthSelect.value)
    const daysInMonth = new Date(year, month, 0).getDate()
    const daysArray = Array.from({ length: daysInMonth }, (_, i) => (i + 1).toString().padStart(2, '0'))

    this._populateSelect(this.daySelect, daysArray, 'дд')
  }
}
