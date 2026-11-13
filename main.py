from bakery import assert_equal
from drafter import *
from dataclasses import dataclass

hide_debug_information()


@dataclass
class Concept:
    """
    A concept, consisting of a term and a definition.
    Used in a Set.
    
    Attributes:
        term (str): The term of the concept, inputted by the user.
        definition (str): The definition of the term, inputted by the user.
    """
    term: str
    definition: str
    
@dataclass
class Set:
    """
    A study set. The study tool allows the user to create sets.
    
    Attributes:
        title (str): The title of the set, inputted by the user.
        concepts (list[Concept]): The list of concepts within the set.
    """
    title: str
    concepts: list[Concept]
    
    
@dataclass
class State:
    """
    The current state of the study tool.
    
    Attributes:
        sets (list[Set]): A list of sets that the user has created.
        current_set (Set): The current set that is being created or studied.
        concept_index (int): The index of the concept that is being studied.
        is_flipped (bool): If the current flashcard is flipped or not.
    """
    sets: list[Set]
    current_set: Set
    concept_index: int
    is_flipped: bool


@route
def index(state: State) -> Page:
    """
    The main page of the study tool. The user can create, view, or study sets.
    Args:
        state (State): The current state of the application.
    Returns:
        Page: The main page of the study tool.
    """
    return Page(state, [
        "Welcome!",
        Button("Create a set", "create_title"),
        Button("View sets", "view_page"),
        Button("Study sets", "study_page")])
        
assert_equal(index(State([], Set("", []), 0, False)), Page(
    State([], Set("", []), 0, False), [
        "Welcome!",
        Button("Create a set", "create_title"),
        Button("View sets", "view_page"),
        Button("Study sets", "study_page")]))


@route
def create_title(state: State) -> Page:
    """
    Lets the user put a title for the set they will create.
    Args:
        state (State): The current state of the application.
    Returns:
        Page: The page for creating the title of the set.
    """
    state.current_set = Set("", [])
    return Page(state, [
        "Enter a title for the set, then click next.",
        TextBox("title"),
        Button("Next", "create_set")])

assert_equal(create_title(State([], Set("", []), 0, False)), Page(
    State([], Set("", []), 0, False), [
        "Enter a title for the set, then click next.",
        TextBox("title"),
        Button("Next", "create_set")]))


@route
def create_set(state: State, title: str) -> Page:
    """
    Lets the user create a set.
    Args:
        state (State): The current state of the application.
        title (str): The title of the set that the user is creating.
    Returns:
        Page: The page for creating a set.
    """
    state.current_set = Set(title, state.current_set.concepts)
    return Page(state, [
        "Enter a term and definition, then click next.",
        "Once you are done making the set, click finish.",
        "\n",
        "Term", " --> ", TextBox("term"),
        "Definition", " --> ", TextBox("definition"),
        Button("Next", "create_concept"),
        Button("Finish", "finish_create")])

assert_equal(create_set(State([], Set("", []), 0, False), "English"), Page(
    State([], Set("English", []), 0, False), [
        "Enter a term and definition, then click next.",
        "Once you are done making the set, click finish.",
        "\n",
        "Term", " --> ", TextBox("term"),
        "Definition", " --> ", TextBox("definition"),
        Button("Next", "create_concept"),
        Button("Finish", "finish_create")]))


@route
def create_concept(state: State, term: str, definition: str) -> Page:
    """
    Takes the term and definition entered from the create_set page,
    makes a Concept, then appends it to State's current_set's concepts.
    Args:
        state (State): The current state of the application.
        term (str): The user's entered term.
        definition (str): The user's entered definition.
    Returns:
        Page: The create_set page, allowing the user to create multiple
        concepts until they are done.
    """
    state.current_set.concepts.append(Concept(term, definition))
    return create_set(state, state.current_set.title)

assert_equal(create_concept(State([], Set("English", []), 0, False), "Verb", "an action"), Page(
    State([], Set("English", [Concept("Verb", "an action")]), 0, False), [
        "Enter a term and definition, then click next.",
        "Once you are done making the set, click finish.",
        "\n",
        "Term", " --> ", TextBox("term"),
        "Definition", " --> ", TextBox("definition"),
        Button("Next", "create_concept"),
        Button("Finish", "finish_create")]))

    
@route
def finish_create(state: State) -> Page:
    """
    Finishes the creation process by appending the created set to State's
    list of sets, as long as the set's list of concepts is not empty.
    Args:
        state (State): The current state of the application.
    Returns:
        Page: The main page of the study tool.
    """
    if len(state.current_set.concepts) > 0:
        state.sets.append(state.current_set)
    return index(state)

assert_equal(finish_create(State([], Set("English", [Concept("Verb", "an action")]), 0, False)), index(
    State([Set("English", [Concept("Verb", "an action")])], Set("English", [Concept("Verb", "an action")]), 0, False)))
    

@route
def view_page(state: State) -> Page:
    """
    Lets the user view the sets they have created.
    If there are no sets in State, the user will receive a special message.
    Args:
        state (State): The current state of the application.
    Returns:
        Page: The page for viewing the user's created sets.
    """
    if len(state.sets) == 0:
        return Page(state, [
            "You haven't created any sets yet.",
            Button("Return", "index")])
                                    
    set_buttons = []
    set_index = 0
    for a_set in state.sets:
        set_buttons.append(Button(a_set.title, "display_set", Argument("index", set_index)))
        set_index += 1
    return Page(state, [
        "Select a set.",
        *set_buttons])

assert_equal(view_page(State([], Set("", []), 0, False)), Page(
    State([], Set("", []), 0, False), [
            "You haven't created any sets yet.",
            Button("Return", "index")]))


@route
def display_set(state: State, index: int) -> Page:
    """
    Lets the user view the terms and defintions from the concepts in the
    set they selected from view_page.
    Args:
        state (State): The current state of the application.
    Returns:
        Page: The page for viewing a selected set.
    """
    concepts = ""
    for concept in state.sets[index].concepts:
        concepts = concepts + "Term: " + concept.term + ", " + "Definition: " + concept.definition + "\n"
    return Page(state, [
        "Set: ",
        state.sets[index].title,
        "\n",
        concepts,
        Button("Home", "index"),
        ])

assert_equal(display_set(State([Set("English", [Concept("Verb", "an action")])], Set("English", [Concept("Verb", "an action")]), 0, False), 0), Page(
    State([Set("English", [Concept("Verb", "an action")])], Set("English", [Concept("Verb", "an action")]), 0, False), [
        "Set: ",
        "English",
        "\n",
        "Term: Verb, Definition: an action\n",
        Button("Home", "index"),
        ]))


@route
def study_page(state: State) -> Page:
    """
    Lets the user select a set to study.
    Args:
        state (State): The current state of the application.
    Returns:
        Page: The page for selecting a set to study.
    """
    if len(state.sets) == 0:
        return Page(state, [
            "You haven't created any sets yet.",
            Button("Return", "index")])
    
    state.concept_index = 0
    set_buttons = []
    set_index = 0
    for a_set in state.sets:
        set_buttons.append(Button(a_set.title, "flashcards", Argument("index", set_index)))
        set_index += 1
    return Page(state, [
        "Select a set.",
        *set_buttons])


@route
def flashcards(state: State, index: int) -> Page:
    """
    Lets the user study the set they selected from study_page in a flashcard format.
    Args:
        state (State): The current state of the application.
        index (int): The index of the current set.
    Returns:
        Page: The page for studying a set with flashcards.
    """
    current_set = state.sets[index]
    card_text = current_set.concepts[state.concept_index].term
    if state.is_flipped:
        card_text = current_set.concepts[state.concept_index].definition
    return Page(state, [
        "Click on the term/definition to flip!",
        Button(card_text, "flip_card", Argument("index", index)),
        Button("Next", "next_flashcard", Argument("index", index)),
        Button("Home", "index")
        ])



@route
def flip_card(state: State, index: int) -> Page:
    """
    Used by the flashcards function to flip a card.
    Args:
        state (State): The current state of the application.
        index (int): The index of the current set.
    Returns:
        Page: The flashcards page, but with the current flashcard flipped.
    """
    state.is_flipped = not state.is_flipped
    return flashcards(state, index)

@route
def next_flashcard(state: State, index: int) -> Page:
    """
    Used by the flashcards function to move to the next card.
    concept_index is changed with modulo to avoid an IndexError and to allow
    the user to loop back to the first flashcard.
    is_flipped is set back to False so that the user starts on the concept's term.
    Args:
        state (State): The current state of the application.
        index (int): The index of the current set.
    Returns:
        Page: The flashcards page, but with the next flashcard.
    """
    state.concept_index = (state.concept_index + 1) % len(state.sets[index].concepts)
    state.is_flipped = False
    return flashcards(state, index)



start_server(State([], Set("", []), 0, False))
