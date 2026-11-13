from manim import *

class MyScene(Scene):
    def construct(self):
        # Create a simple text object
        text = Text("Hello, Manim!")
        
        # Display the text on the screen
        self.play(Write(text))
        
        # Wait for a moment before ending the scene
        self.wait(2)

        # Display the text being unwritten from the scene
        self.play(Unwrite(text))
        self.wait()

class MyOtherScene(Scene):
    def construct(self):
        # Create Mobject to display a scalar, a vector, and a matrix
        scalar = MathTex("a").next_to(ORIGIN, UP)
        vector = MathTex(r"\vec{v} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}").next_to(scalar, RIGHT)
        matrix = MathTex(r"M = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}").next_to(vector, RIGHT)
        # Manually setting an alignment of the three mobjects to be centered on the screen, organized horizontally
        group = VGroup(scalar, vector, matrix).arrange(RIGHT, buff=1).move_to(ORIGIN)
        # Placing titles above each mobject to delinate them
        scalar_title = Text("Scalar")
        vector_title = Text("Vector")
        matrix_title = Text("Matrix")
        title_group = VGroup(scalar_title, vector_title, matrix_title).arrange(RIGHT, buff=1.5).next_to(group, UP)


        # Display the scalar, vector, and matrix on the screen
        self.play(Write(scalar_title))
        self.play(Write(scalar))
        self.wait()
        self.play(Write(vector_title))
        self.play(Write(vector))
        self.wait()
        self.play(Write(matrix_title))
        self.play(Write(matrix))
        self.wait()