Book Club App 

created by Guy Chaplin for CS50 in May/ June 2019.

DESCRIPTION

The book club app is designed for members of a book club who want to promote a book for forthcoming meetings.

FEATURES

The 'home' page shows books already promoted for the group. The listing includes book title and author along with the
date of the meeting. The book cover image is displayed along with a description of the book.

The 'query' page allows members to search for a book based on author, title or subject. After searching for a book the options are
returned and the member can select their book and choose a meeting date.

The new book is added to the 'meetings' page. (The same as the 'home' page).

IMPLEMENTATION

The app draws on the Python/Flask framework provided by the Finance Problem Set. It uses the same register/login/logout functions provided there.
The book information is provided by the Google Books API. It accesses and searches their public database of books.