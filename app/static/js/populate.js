let select = document.querySelector('inputMajor');

let major_category = [
  'Agriculture & Natural Resources',
  'Arts',
  'Biology & Life Science',
  'Communications & Journalism',
  'Computers & Mathematics',
  'Education',
  'Engineering',
  'Humanities & Liberal Arts',
  'Industrial Arts & Consumer Services',
  'Law & Public Policy',
  'Physical Sciences',
  'Psychology & Social Work',
  'Social Science',
];

let options = major_category
    .map((major) => `<option value=${major}>${major}</option>`)
    .join('\n');
select.innerHTML = options;

