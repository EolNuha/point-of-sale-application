class Pagination {
  constructor() {
    this.items = null;
    this.page_range = [];
    this.has_next = false;
    this.has_prev = false;
    this.next_num = null;
    this.prev_num = null;
    this.page = null;
    this.pages = null;
    this.per_page = null;
    this.total = null;
  }
  fromData(data) {
    this.items = data.items || null;
    this.page_range = data.page_range || [];
    this.has_next = data.has_next || false;
    this.has_prev = data.has_prev || false;
    this.next_num = data.next_num || null;
    this.prev_num = data.prev_num || null;
    this.page = data.page || null;
    this.pages = data.pages || null;
    this.per_page = data.per_page || null;
    this.total = data.total || null;
  }
}

export default Pagination;
