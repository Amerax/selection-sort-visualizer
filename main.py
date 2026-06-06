import simplegui

numbers = []
n = 0
i = 0
j = 0
min_idx = 0
sorting_started = False
sorting_done = False
status_message = "Enter up to 8 numbers (e.g., 5,3,8,1) and press Enter/Update."

WIDTH = 600
HEIGHT = 400

def parse_input(text_input):
    """Parses the user input into a list of integers."""
    global numbers, n, i, j, min_idx, sorting_started, sorting_done, status_message
    try:
        parsed = [int(x.strip()) for x in text_input.split(",") if x.strip() != ""]
        
        if len(parsed) == 0:
            status_message = "Please enter at least one number."
            return
        elif len(parsed) > 8:
            status_message = "Too many numbers! Please enter 8 or fewer."
            return
            
        numbers = parsed
        n = len(numbers)
        i = 0
        j = 1
        min_idx = 0
        sorting_started = False
        sorting_done = False
        status_message = "Loaded list. Click 'Next Step' to start sorting."
    except ValueError:
        status_message = "Invalid input! Please use numbers separated by commas."

def next_step():
    """Advances the selection sort algorithm by one step."""
    global i, j, min_idx, sorting_started, sorting_done, status_message, numbers
    
    if len(numbers) == 0:
        status_message = "Please enter some numbers first!"
        return
    if sorting_done:
        status_message = "Sorting already complete!"
        return
        
    if not sorting_started:
        sorting_started = True
        i = 0
        min_idx = i
        j = i + 1
        status_message = "Starting scan. Initial minimum is at index " + str(min_idx) + "."
        return

    if i < n - 1:
        if j < n:
            status_message = "Comparing index " + str(j) + " with current minimum at index " + str(min_idx) + "."
            if numbers[j] < numbers[min_idx]:
                min_idx = j
                status_message += " New minimum found at index " + str(min_idx) + "!"
            j += 1
        else:
            status_message = "Swapping element at index " + str(i) + " with minimum at index " + str(min_idx) + "."
            numbers[i], numbers[min_idx] = numbers[min_idx], numbers[i]
            
            i += 1
            min_idx = i
            j = i + 1
            
            if i >= n - 1:
                sorting_done = True
                status_message = "Sorting complete! All elements are in order."
    else:
        sorting_done = True
        status_message = "Sorting complete! All elements are in order."

def draw(canvas):
    """Draws the bars, values, and current state onto the canvas."""
    if len(numbers) == 0:
        canvas.draw_text("No data loaded.", (50, 200), 24, "Gray")
        canvas.draw_text(status_message, (30, 350), 16, "White")
        return

    bar_width = (WIDTH - 100) / len(numbers)
    
    max_val = max(numbers) if max(numbers) > 0 else 1
    
    for idx in range(len(numbers)):
        x0 = 50 + idx * bar_width
        x1 = x0 + bar_width - 10
        
        height = (numbers[idx] / max_val) * 150 + 20
        y0 = 280 - height
        y1 = 280
        
        color = "LightBlue" 
        
        if sorting_started and not sorting_done:
            if idx < i:
                color = "LightGreen"   
            elif idx == min_idx:
                color = "Red"          
            elif idx == j - 1:
                color = "Yellow"       
        elif sorting_done:
            color = "LightGreen"      

        canvas.draw_polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], 1, "White", color)
        
        canvas.draw_text(str(numbers[idx]), (x0 + (bar_width-10)/2 - 5, y0 - 10), 18, "White")
        
        canvas.draw_text("Idx " + str(idx), (x0 + (bar_width-10)/2 - 15, y1 + 20), 12, "Gray")

    canvas.draw_text(status_message, (30, 350), 16, "Gold")
    
    if sorting_started and not sorting_done:
        canvas.draw_text("Red: Min | Yellow: Comparing | Green: Sorted", (30, 20), 14, "Gray")

frame = simplegui.create_frame("Selection Sort Visualizer", WIDTH, HEIGHT)

frame.add_input("Enter numbers (max 8, comma separated):", parse_input, 200)
frame.add_button("Next Step", next_step, 150)

frame.set_draw_handler(draw)

frame.start()
