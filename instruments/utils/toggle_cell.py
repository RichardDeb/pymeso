from IPython.core.display import display, HTML

toggle_code_str = '''
    <form action="javascript:code_toggle()"><input type="submit" id="toggleButton" value="Hide/Show"></form>
    '''
toggle_code_prepare_str = '''
<script>
function code_toggle() {
    if ($('div.cell.code_cell.rendered.selected div.input').css('display')!='none'){
        $('div.cell.code_cell.rendered.selected div.input').hide();
    } else {
        $('div.cell.code_cell.rendered.selected div.input').show();
    }
}
</script>

'''

display(HTML(toggle_code_prepare_str+toggle_code_str))

def hide_button():
    '''
        function used to hide the input cell
    '''
    
    display(HTML(toggle_code_str))