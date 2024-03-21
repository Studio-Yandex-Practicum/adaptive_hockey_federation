class Selector {
  constructor(availableItems, elements) {
    this.availableItems = availableItems
    this.selectedItems = []

    this.availableList = document.getElementById(elements.availableList)
    this.selectedList = document.getElementById(elements.selectedList)
    this.deleteAllButton = document.getElementById(elements.deleteAllButton)
    this.selectAllButton = document.getElementById(elements.selectAllButton)
    this.searchAvailableInput = document.getElementById(elements.searchAvailableInput)
    this.searchSelectInput = document.getElementById(elements.searchSelectInput)

    this._initialize()
  }

  _initialize() {
    this._renderAvailableItems()
    this._renderSelectedItems()
    this._setupEventListeners()
  }

  _renderAvailableItems() {
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
        li.addEventListener('click', () => this._toggleSelection(item))
        this.availableList.appendChild(li)
      }
    })
  }

  _renderSelectedItems() {
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
        li.addEventListener('click', () => this._toggleSelection(item))
        this.selectedList.appendChild(li)
      }
    })
  }

  _toggleSelection(item) {
    if (this.selectedItems.includes(item)) {
      this.selectedItems = this.selectedItems.filter(
        selectedItem => selectedItem !== item
      )
    } else {
      this.selectedItems.push(item)
    }
    this._renderSelectedItems()
  }

  _setupEventListeners() {
    this.deleteAllButton.addEventListener('click', () => this._removeAll())
    this.selectAllButton.addEventListener('click', () => this._selectAll())
    this.searchAvailableInput.addEventListener('input', () =>
      this._renderAvailableItems()
    )
    this.searchSelectInput.addEventListener('input', () =>
      this._renderSelectedItems()
    )
  }

  _selectAll() {
    this.selectedItems = [...this.availableItems]
    this._renderSelectedItems()
  }

  _removeAll() {
    this.selectedItems = []
    this._renderSelectedItems()
  }

  getSelectedItems() {
    return this.selectedItems
  }
}
