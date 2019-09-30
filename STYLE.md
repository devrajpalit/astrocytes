# STYLE

1. Each component must be in a separate class, in a separate file
2. Each component must have a `render` method.
  1. The `render` method must only be concerned with rendering the component and nothing else.
  2. If data manipulation is needed, separate method must be created and called.
3. In each component class, member functions must be placed alphabetically. The `render` method must be placed at the bottom.
4. Any sub-render method (ex: `render_button`, `render_title` etc) must be placed before render, in alphabetically.
5. Any data that belongs to any of the following categories, must be kept in `utils.py`:
  1. Needed frequently
  2. Needed in multiple components
  3. Loaded from a file (ex: audio, images, fonts etc)
6. Each component that is concerned with pygame events must have an `event_handler` method, which may call other member functions
7. The `event_handler` member must be placed right after `__init__`
8. Importing modules must be broken into following categories, alphabetically:
  1. Import from `utils.py`
  2. Python packages
  3. Components (Button, Text, Menu etc)
9. In any category, `from X import Y` must be placed above `import X`
10. If, at any point, line-width exceeds 80 characters, write all items in multiple lines, wrapped in parenthesis. The closing parenthesis must stay with last item.
