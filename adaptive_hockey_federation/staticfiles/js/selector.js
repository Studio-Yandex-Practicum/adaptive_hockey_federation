class Selector {
  constructor(availableItems, elements, selectItems) {
    this.availableItems = availableItems
    this.selectedItems = selectItems || []

    this.availableItems = this.availableItems.filter(
      item => !this.selectedItems.includes(item)
    )

    this.elements = elements
    this.availableList = elements.availableList
    this.selectedList = elements.selectedList
    this.deleteAllButton = elements.deleteAllButton
    this.selectAllButton = elements.selectAllButton
    this.searchAvailableInput = elements.searchAvailableInput
    this.searchSelectInput = elements.searchSelectInput

    this.initialize()
  }

  initialize() {
    this.renderAvailableItems()
    this.renderSelectedItems()
    this.setupEventListeners()
  }

  renderAvailableItems() {
    this.availableList.innerHTML = ''
    this.availableItems.forEach(item => {
      if (
        this.searchAvailableInput.value.trim() === '' ||
        item
          .toLowerCase()
          .includes(this.searchAvailableInput.value.toLowerCase().trim())
      ) {
        const li = document.createElement('li')
        li.classList.add('selector-item')
        li.textContent = item
        li.addEventListener('click', () => this.toggleSelection(item))
        this.availableList.appendChild(li)
      }
    })
  }

  renderSelectedItems() {
    this.selectedList.innerHTML = ''
    this.selectedItems.forEach(item => {
      if (
        this.searchSelectInput.value.trim() === '' ||
        item
          .toLowerCase()
          .includes(this.searchSelectInput.value.toLowerCase().trim())
      ) {
        const li = document.createElement('li')
        li.classList.add('selector-item')
        li.textContent = item
        li.addEventListener('click', () => this.toggleSelection(item))
        this.selectedList.appendChild(li)
      }
    })
  }

  toggleSelection(item) {
    if (this.selectedItems.includes(item)) {
      this.selectedItems = this.selectedItems.filter(
        selectedItem => selectedItem !== item
      )
      this.availableItems.push(item)
    } else {
      this.selectedItems.push(item)
      this.availableItems = this.availableItems.filter(
        availableItem => availableItem !== item
      )
    }
    this.renderSelectedItems()
    this.renderAvailableItems()
  }

  setupEventListeners() {
    this.deleteAllButton.addEventListener('click', () => this.removeAll())
    this.selectAllButton.addEventListener('click', () => this.selectAll())
    this.searchAvailableInput.addEventListener('input', () =>
      this.renderAvailableItems()
    )
    this.searchSelectInput.addEventListener('input', () =>
      this.renderSelectedItems()
    )
  }

  selectAll() {
    this.selectedItems = [...this.availableItems]
    this.availableItems = []
    this.renderSelectedItems()
    this.renderAvailableItems()
  }

  removeAll() {
    this.availableItems = [...this.availableItems, ...this.selectedItems]
    this.selectedItems = []
    this.renderSelectedItems()
    this.renderAvailableItems()
  }

  getSelectedItems() {
    return this.selectedItems
  }
}