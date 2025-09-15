# AlgorithmVisualisation
This project was created as a teaching aid for the programming subject of the 10th Grade in Kantonsschule Zürich Nord
To start the project, given an installation of python, the required libraries can be installed as followed:

```console
pip install -r requirements.txt
```

To run the App simply execute the gui.py python file

# Navigation
In the App, the top most drop down menu determines which type of algorithms are currently being viewed.

The two types are Sorting and Searching


## Sorting
In the Sorting page, the leftmost button generates a new random array, the bars representing the numbers, the length being the representation of the value of the number. 

The dropdown menu that follows is for the choice of sorting algorithms.

Then the button to launch the sorting and the dropdown menu for the size of the list can be found. The sizes 8 and 16 allow for manual sorting testing with the bottom most row of buttons.

## Searching
On the Searching page it works similarly as on the Sorting page, with the exception of a new button for sorting the list. This button is to allow binary search to work, since it requires a sorted list. 

Similarly to the Sorting page, the bottom most row works for manual search, and works only on sizes 8 and 16

# Own implementations of Algorithms
Per default, the implemented algorithms will be already loaded in, but to test own implementation capabilities, the file, from which "Sort_Worker" and "Search_Worker" are imported, has to be changed, by uncommenting the line 11 and commenting line 10. 

In the file "implement_algorithms.py", in the TODO areas, the code can be used. 

The draw_switch() function for sorting and draw_guess() function for searching can be used to display the indices which are being switched, with the time to wait inbetween operations for sorting and the index which has been guessed and the time between operations for searching respectively.

The function draw_comparison() takes the same parameters as draw_switch, the two indices being compared and the time between operations, which can help to visualize which indices are being currently compared.