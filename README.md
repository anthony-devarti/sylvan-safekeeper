# sl-db
database for sylvan library


this is the backend for the project found here: https://github.com/anthony-devarti/sylvan-library

## A very early db diagram
![sl diagram](https://github.com/anthony-devarti/sl-db/assets/98314025/9a8ecd24-c08b-454c-b49a-ee8d8799a65d)


## Notes on backend:
<ul>We want cards to be reserved immediately when a user adds them to their basket
  <li>Make sure if this happens, a card cannot be reserved forever</li>
  <li>This means that LineItem is updated immediately onClick of Reserve button </li></ul>
