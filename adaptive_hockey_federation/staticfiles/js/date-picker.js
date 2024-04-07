class DatePicker {
  constructor(yearSelect, monthSelect, daySelect) {
    this.yearSelect = yearSelect
    this.monthSelect = monthSelect
    this.daySelect = daySelect
    this.init()
  }

  init() {
    this.populateSelect(this.yearSelect, this.getYears(), 'гггг')
    this.populateSelect(this.monthSelect, this.getMonths(), 'мм')
    this.updateDays()

    this.yearSelect.addEventListener('change', () => this.updateDays())
    this.monthSelect.addEventListener('change', () => this.updateDays())
  }

  getYears() {
    const currentYear = new Date().getFullYear()
    return Array.from({length: currentYear - 1999}, (_, i) => currentYear - i)
  }

  getMonths() {
    return Array.from({length: 12}, (_, i) => (i + 1).toString().padStart(2, '0'))
  }

  populateSelect(selectElement, optionsArray, defaultValue) {
    selectElement.innerHTML = `<option value="" disabled selected>${defaultValue}</option>` + optionsArray.map(
      option => `<option value="${option}">${option}</option>`
    ).join('')
  }

  updateDays() {
    const year = parseInt(this.yearSelect.value)
    const month = parseInt(this.monthSelect.value)
    const daysInMonth = new Date(year, month, 0).getDate()
    const daysArray = Array.from({length: daysInMonth}, (_, i) => (i + 1).toString().padStart(2, '0'))

    this.populateSelect(this.daySelect, daysArray, 'дд')
  }
}
