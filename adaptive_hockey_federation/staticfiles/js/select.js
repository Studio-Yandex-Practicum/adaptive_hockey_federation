class SelectManipulation {
  constructor(id_select_available, id_select_current) {
    this.select_available = document.getElementById(id_select_available);
    this.select_current = document.getElementById(id_select_current);

    this.cache = null;

    this.addEventListeners();
  }

  addEventListeners() {
    this.select_available.addEventListener('dblclick', () => {
      this.moveOption(this.select_available, this.select_current);
    });

    this.select_current.addEventListener('dblclick', () => {
      this.moveOption(this.select_current, this.select_available);
    });
  }

  moveOption(select_available, select_current) {
    const selectedOption = select_available.options[select_available.selectedIndex];
    if (selectedOption) {
      select_current.appendChild(selectedOption);
    }
  }
}

class SearchValue {
  constructor(id_select, id_filter) {
    this.select = document.getElementById(id_select);
    this.input = document.getElementById(id_filter);

    this.addEventListeners();
  }

  addEventListeners() {
      this.input.addEventListener('input', () => {
        this.searchText(this.input);
      });
  }

  searchText() {
    const searchText = this.input.value.toLowerCase();
    const options = this.select.getElementsByTagName('option');
    for (let i = 0; i < options.length; i++) {
        const optionText = options[i].innerText.toLowerCase();
        if (optionText.includes(searchText)) {
            options[i].style.display = '';
        } else {
            options[i].style.display = 'none';
        }
    }
  }
}

class SelectAllSelected {
  constructor(id) {
    this.select = document.getElementById(id);

    this.addAllSelected();

    this.select.addEventListener('dblclick', () => {
      this.updateSelectedOptions();
    });
    this.select.addEventListener('blur', () => {
      this.addAllSelected();
    });
  }

  addAllSelected() {
    for (let i = 0; i < this.select.options.length; i++) {
      this.select.options[i].selected = true;
    }
  }

  updateSelectedOptions() {
    for (let i = 0; i < this.select.options.length; i++) {
      if (!this.select.options[i].selected) {
        this.select.options[i].selected = true;
      }
    }
  }
}
