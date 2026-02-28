import streamlit as st
from abc import ABC, abstractmethod

class Widget(ABC):
    def __init__(self, widget_id, title):
        self.wid = widget_id
        self.title = title
        
        if f'{self.wid}_is_expanded' not in st.session_state:
            st.session_state[f'{self.wid}_is_expanded'] = False

        if f'{self.wid}_output' not in st.session_state:
            st.session_state[f'{self.wid}_output'] = None

    @abstractmethod
    def render_inputs(self):
        pass

    def render_outputs(self):
        st.write(f'### {self.title} Results')
        data = st.session_state[f'{self.wid}_output']

        raw, table, image = st.tabs(["Raw Result", "Table", "Image"])

        with raw:
            if data:
                st.code(data.get('raw', "No data"))
        with table:
            if data:
                st.dataframe(data.get('table', []))
        with image:
            if data:
                st.image(data.get('image_path', 'https://via.placeholder.com/150'))

    def render_pin_button(self):
        if st.button("Pin to Top", key=f'{self.wid}_pin'):
            st.session_state.pinned_widget_id = self.wid
            st.rerun()

    def run(self):
        actual_expand_state = st.session_state[f'{self.wid}_is_expanded']

        with st.expander(self.title, expanded=actual_expand_state):
            self.render_pin_button()
            self.render_inputs()
            st.divider()
            if st.session_state[f'{self.wid}_output']:
                self.render_outputs()

class TextQueryWidget(Widget):
    def render_inputs(self):
        if st.button("Toggle Full Width", key=f'{self.wid}_sz'):
            st.session_state[f'{self.wid}_is_expanded'] = not st.session_state[f'{self.wid}_is_expanded']
            st.rerun()

        query = st.text_input("Enter Query", key=f'{self.wid}_text')
        if st.button("Process Text", key=f'{self.wid}_btn'):
            ascii_sum = sum(ord(q) for q in query)
            max_letter = chr(max(ord(q) for q in query))
            min_letter = chr(min(ord(q) for q in query))
            letters = [q for q in query if q != " "]
            mode_letter = sorted(((l, letters.count(l)) for l in letters), key=lambda x: x[1])[-1][0]
            result = {
                "sum": ascii_sum,
                "max": max_letter,
                "min": min_letter,
                "mode": mode_letter,
            }
            st.session_state[f'{self.wid}_output'] = {
                "raw": str(result),
                "table": [result],
            }

class RadioSelectionWidget(Widget):
    def render_inputs(self):
        if st.button("Toggle Full Width", key=f'{self.wid}_sz'):
            st.session_state[f'{self.wid}_is_expanded'] = not st.session_state[f'{self.wid}_is_expanded']
            st.rerun()

        text = st.text_input("Enter Text", key=f'{self.wid}_text_with_radio')
        choice = st.radio("Choose Transformation", ["Upper", "Title", "Lower"], key=f'{self.wid}_radio')
        if st.button("Transform", key=f'{self.wid}_btn'):
            result = None
            match choice:
                case "Upper":
                    result = text.upper()
                case "Title":
                    result = text.title()
                case "Lower":
                    result = text.lower()
                case _:
                    result = text

            output = {'original': text, 'choice': choice, 'result': result}

            st.session_state[f'{self.wid}_output'] = {
                "raw": str(output),
                "table": [output]
            }


class WidgetManager:
    def __init__(self):
        if "widgets" not in st.session_state:
            st.session_state.widgets = [
                TextQueryWidget("w1", "Data Search"),
                TextQueryWidget("w2", "Another Data Search"),
                RadioSelectionWidget("w3", "Text Transform"),
                RadioSelectionWidget("w4", "Another Text Transform")
            ]

        if "pinned_widget_id" not in st.session_state:
            st.session_state.pinned_widget_id = None

        if "force_grid" not in st.session_state:
            st.session_state.force_grid = False


    def get_ordered_widgets(self):
        pinned_id = st.session_state.pinned_widget_id

        result = sorted(st.session_state.widgets, key=lambda x: (x.wid != pinned_id, int(x.wid[1:])))
        return result


    def collapse_all_widgets(self):
        for widget in st.session_state.widgets:
            st.session_state[f"{widget.wid}_is_expanded"] = False

    def render_smart_grid(self):
        app_title, _, clear_pin, reset_col = st.columns([2, 6, 2, 2])
        with app_title:
            st.title("My App")
        with clear_pin:
            if st.button("Clear Pin", use_container_width=True):
                st.session_state.pinned_widget_id = None
                st.rerun()
        with reset_col:
            label = "Restore Custom Layout" if st.session_state.force_grid else "Reset Grid Layout"
            if st.button(label, use_container_width=True):
                st.session_state.force_grid = not st.session_state.force_grid
                st.rerun()

        st.divider()

        collapsed_queue = []

        for widget in self.get_ordered_widgets():
            is_expanded = st.session_state[f'{widget.wid}_is_expanded']
            is_pinned = (widget.wid == st.session_state.pinned_widget_id)

            if is_expanded and not st.session_state.force_grid:
                self._flush_collapsed(collapsed_queue)
                widget.run()
            else:
                collapsed_queue.append(widget)
                if len(collapsed_queue) == 3:
                    self._flush_collapsed(collapsed_queue)

        self._flush_collapsed(collapsed_queue)

    def _flush_collapsed(self, queue):
        if not queue:
            return

        cols = st.columns([1 for _ in range(len(queue))])
        for i, widget in enumerate(queue):
            with cols[i]:
                widget.run()

        queue.clear()


def main():
    st.set_page_config(layout="wide")

    manager = WidgetManager()
    manager.render_smart_grid()


if __name__ == "__main__":
    main()
