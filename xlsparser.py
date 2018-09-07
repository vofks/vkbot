import xlrd
from copy import deepcopy

def explore_block(book, sheet, hidden_cols, cell_row, cell_col, visited=None):
    if visited is None:
        visited = set([(cell_row, cell_col)])
    else:
        if (cell_row, cell_col) in visited:
            return
        else:
            visited.add((cell_row, cell_col))
    top = has_top_border(book, sheet, hidden_cols, cell_row, cell_col)
    bottom = has_bottom_border(book, sheet, hidden_cols, cell_row, cell_col)
    left = has_left_border(book, sheet, hidden_cols, cell_row, cell_col)
    right = has_right_border(book, sheet, hidden_cols, cell_row, cell_col)

    borders = [top, bottom, left, right]
    cells = [(cell_row - 1, cell_col),
             (cell_row + 1, cell_col),
             (cell_row, cell_col - 1),
             (cell_row, cell_col + 1)]
    for i in range(4):
        if borders[i] == 0:
            next_cell_row, next_cell_col = cells[i]
            explore_block(book, sheet, hidden_cols, next_cell_row, next_cell_col, visited)

    return visited


def has_left_border(book, sheet, hidden_cols, row, col):
    cell1 = sheet.cell(row, col)
    cell2 = sheet.cell(row, col - 1)
    fmt1 = book.xf_list[cell1.xf_index]
    fmt2 = book.xf_list[cell2.xf_index]
    if (col - 1) in hidden_cols:
        return True
    if fmt1.border.left_line_style != 0 or fmt2.border.right_line_style != 0:
        return True
    return False


def has_right_border(book, sheet, hidden_cols, row, col):
    cell1 = sheet.cell(row, col)
    cell2 = sheet.cell(row, col + 1)
    fmt1 = book.xf_list[cell1.xf_index]
    fmt2 = book.xf_list[cell2.xf_index]
    if (col + 1) in hidden_cols:
        return True
    if fmt1.border.right_line_style != 0 or fmt2.border.left_line_style != 0:
        return True
    return False


def has_top_border(book, sheet, hidden_cols, row, col):
    cell1 = sheet.cell(row, col)
    cell2 = sheet.cell(row - 1, col)
    fmt1 = book.xf_list[cell1.xf_index]
    fmt2 = book.xf_list[cell2.xf_index]
    return fmt1.border.top_line_style != 0 or fmt2.border.bottom_line_style != 0


def has_bottom_border(book, sheet, hidden_cols, row, col):
    cell1 = sheet.cell(row, col)
    cell2 = sheet.cell(row + 1, col)
    fmt1 = book.xf_list[cell1.xf_index]
    fmt2 = book.xf_list[cell2.xf_index]
    return fmt1.border.bottom_line_style != 0 or fmt2.border.top_line_style != 0

def get_groups_blocks(book,sheet,hidden_cols):
    group_row = 12
    begin_col = 4
    groups = {}
    for col in range(begin_col,sheet.ncols-2):
        if col in hidden_cols:
            continue
        cell = sheet.cell(group_row,col)
        value = cell.value
        value = value.replace(" ","")
        if value != "":
            groups[value] = explore_block(book,sheet,hidden_cols,group_row,col)
    return groups


def get_group_cols(group,groups_blocks):
    group_block = groups_blocks[group]
    max,min=-1,100000
    for cell in group_block:
        if cell[1]<min:
            min = cell[1]
        if cell[1]>max:
            max = cell[1]
    return tuple(i for i in range(min,max+1))

def print_block(sheet,block):
    for cell_coords in block:
        cell = sheet.cell(cell_coords[0], cell_coords[1])
        if cell.value:
            print(cell.value)

def block_to_pair(sheet,block):
    res = []
    for cell_coords in block:
        cell = sheet.cell(cell_coords[0], cell_coords[1])
        if cell.value:
            res.append(cell.value)
    return res


def get_times(sheet): #["ПН"][<пара>-1][<true, если верхняя неделя>] = <строка>
    times_col = 1
    begin_row = 15
    end_row = 111
    week_days = ["ПН","ВТ","СР","ЧТ","ПТ","СБ"]
    current_day = -1
    pair = 1
    is_up_week = True
    times = {i:[{} for i in range(8)] for i in week_days}
    for row in range(begin_row,end_row+1):
        value = sheet.cell(row,times_col).value
        if not value:
            continue
        if value==0.3125:#7:30
            current_day+=1
            pair = 1
            is_up_week = True
        times[week_days[current_day]][pair-1][is_up_week] = row
        if not is_up_week:
            pair+=1
        is_up_week = not is_up_week
    return  times

def get_schedule_for_group(book,sheet,hidden_cols,times,groups_blocks,group_col):
    week_days = ["ПН","ВТ","СР","ЧТ","ПТ","СБ"]
    schedule = deepcopy(times)
    for day in week_days:
        for pair in range(8):
            up_row = times[day][pair][True]
            down_row = times[day][pair][False]
            schedule[day][pair] = (block_to_pair(sheet,explore_block(book,sheet,hidden_cols,up_row,group_col)) ,
                                   block_to_pair(sheet,explore_block(book, sheet, hidden_cols, down_row, group_col)) )
    return schedule


def get_hidden_cols(sheet):
    hidden_cols = []
    for i in range(sheet.ncols):
        if sheet.colinfo_map[i].hidden == 1:
            hidden_cols.append(i)
    return hidden_cols


def get_schedule_for_all(file):
    rb = xlrd.open_workbook(file, formatting_info=True)
    sheet = rb.sheet_by_index(0)
    hidden_cols = get_hidden_cols(sheet)
    gb = get_groups_blocks(rb,sheet,hidden_cols)
    times = get_times(sheet)
    schedule = {}
    for group in gb:
        group_cols = get_group_cols(group, gb)
        schedule[group] = [get_schedule_for_group(rb,sheet,hidden_cols,times,gb,sub_group_col) for sub_group_col in group_cols]
    return schedule


def get_beautiful_schedule_for_group(group,sub_group,is_up_week,schedule):
    is_up_week = int(not is_up_week)
    schedule = schedule[group][sub_group-1]
    res = ""
    for day in schedule:
        res += day +"\n"
        for pair in range(len(schedule[day])):
            res += "  пара №%d : %s" %(pair+1,schedule[day][pair][is_up_week]) + "\n"
    return res



if __name__ == "__main__":
    sh = get_schedule_for_all("raspisanie_bakalavry-6.xls")
    print(get_beautiful_schedule_for_group("381802",1,True,sh))
