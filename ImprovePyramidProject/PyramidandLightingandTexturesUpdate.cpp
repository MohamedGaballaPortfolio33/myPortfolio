#include  <GLEW/glew.h>
#include <GLFW/glfw3.h>
#include <iostream>

//GLM Libariries 
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include  <glm/gtc/type_ptr.hpp>

#include <SOIL2/SOIL2.h>


using namespace std;

int width, height;
const double PI = 3.14159;
const float toRadians = PI / 180.0f;

//Input Function prototypes
void key_callback(GLFWwindow* window, int key, int scancode, int action, int mods);
void scroll_callback(GLFWwindow* window, double xoffset, double yoffset);
void cursor_position_callback(GLFWwindow* window, double xpos, double ypos);
void mouse_button_callback(GLFWwindow* window, int button, int action, int mods);

//Declare View Matrix
glm::mat4 viewMatrix;

//Initialize FOV
GLfloat fov = 45.f;

//Define Camera Attributes
glm::vec3 cameraPosition = glm::vec3(0.f, 0.f, 3.f);
glm::vec3 cameraPosition2 = glm::vec3(0.f, 0.f, 3.f);
glm::vec3 target = glm::vec3(0.f, 0.f, 0.f);
glm::vec3 cameraDirection = glm::normalize(cameraPosition - target);
glm::vec3 worldUp = glm::vec3(0.f, 1.f, 0.f);
glm::vec3 cameraRight = glm::normalize(glm::cross(worldUp, cameraDirection));
glm::vec3 cameraUp = glm::normalize(glm::cross(cameraDirection, cameraRight));
glm::vec3 cameraFront = glm::normalize(glm::vec3(0.f, 0.f, -1.f));

//Declare target prototype
glm::vec3 getTarget();

// Camera transformation prototype
void TransformCamera();

//Boolean for keys and mouse buttons
bool keys[1024], mouseButtons[3];

// Boolean to check camera transformations
bool isPanning = false, isOrbiting = false;

//Radius Pitch, and Yaw
GLfloat radius = 3.f, rawYaw = 0.f, rawPitch = 0.f, degYaw, degPitch;

GLfloat deltaTime = 0.f;
GLfloat lastFrame = 0.f;
GLfloat lastX = 320, lastY = 240, xChange, yChange;// Center mouse cursor

bool firstMouseMove = true; //Detect initial mouse movement

glm::vec3 lightPosition(0.0f, 1.0f, 0.0f);
void initCamera();
//Draw Primitive(s)
void draw()
{
	GLenum node = GL_TRIANGLES;
	GLsizei indices = 6;

	glDrawElements(node, indices, GL_UNSIGNED_BYTE, nullptr);


}

//Create and Compile Shaders
static GLuint CompileShader(const string& source, GLuint shaderType)
{
	//Create Shader object
	GLuint shaderID = glCreateShader(shaderType);
	const char* src = source.c_str();

	//Attach source code to Shader object
	glShaderSource(shaderID, 1, &src, nullptr);

	//Compile Shader
	glCompileShader(shaderID);

	//Return ID of Compiled Shader
	return shaderID;


}
//Create Program Object
static GLuint CreateShaderProgram(const string& vertexShader, const string& fragmentShader)
{
	//Compile vertex Shader
	GLuint vertexShaderComp = CompileShader(vertexShader, GL_VERTEX_SHADER);

	//Compile Fragment Shader
	GLuint fragmentShaderComp = CompileShader(fragmentShader, GL_FRAGMENT_SHADER);

	//Create program object
	GLuint shaderProgram = glCreateProgram();

	//Attach vertex and fragment shaders to program object
	glAttachShader(shaderProgram, vertexShaderComp);
	glAttachShader(shaderProgram, fragmentShaderComp);

	// Link shaders to create executable
	glLinkProgram(shaderProgram);

	//Delete vertex and fragment shaders
	glDeleteShader(vertexShaderComp);
	glDeleteShader(fragmentShaderComp);

	//Return Shader Program
	return shaderProgram;

}
int main(void)
{
	width = 640;
	height = 480;
	GLFWwindow* window;


	/*From Initializing the library of the GLFW the if statement
	will setup the library to use for adding the library for the include and the
	lib-vc2015 to be inserted for the following code*/
	if (!glfwInit())
		return -1;

	/*The method below is used for creating a window and to provide it context to the window */
	window = glfwCreateWindow(width, height, "Mohamed Gaballa", NULL, NULL);
	/*The second if statement will help us to create the window context when
	running the code. It will help the window to appear once the program compliers.*/
	if (!window)
	{
		glfwTerminate();
		return -1;
	}
	//Set Input callback functions
	glfwSetKeyCallback(window, key_callback);
	glfwSetCursorPosCallback(window, cursor_position_callback);
	glfwSetMouseButtonCallback(window, mouse_button_callback);
	glfwSetScrollCallback(window, scroll_callback);

	/*The following method will help to make the window to use the current
	size and color of the window's context.*/
	glfwMakeContextCurrent(window);
	// Initialize GLEW
	if (glewInit() != GLEW_OK)
		cout << "Error" << endl;
	//Adding the same vertices from the GLfloat to be used as the lampVertices.
	GLfloat lampVertices[] =
	{    //Indices 0
		-0.5, 0.0, 0.0,
		//Indeces 1
		0.0, 1.0, 0.0,
		//Indices 2
		0.5, 0.0, 0.0,
	};

	//The vertices are used to create the structure of the Pyramid design
	GLfloat vertices[] = {
		//Triangle 1
		// Index 0
		-0.5, 0.0, 0.0,
		//red
		1.0, 0.0, 0.0,
		//UV (bL)
		 0.5, 0.0,
		 // normal positive z
		 0.0f, 0.0f, 1.0f,

		 //Index 1
		 0.0, 1.0, 0.0,
		 //green
		 0.0, 1.0, 0.0,
		 //UV (tl)
		 0.0, 1.0,
		 // normal positive z
		 0.0f, 0.0f, 1.0f,

		 //2
		 0.5, 0.0, 0.0,
		 //blue
		 1.0, 0.0, 1.0,
		 // UV(br)
		 1.0, 0.5,
		 // normal positive z
		 0.0f, 0.0f, 1.0f,
	};
	//Define element indices that is used to define the vertices 
	//to help to create the Pyramid design
	GLubyte indices[] = {
		0,1,2,
	};

	// Plane positions these posisitions are used to help 
	//adjust the location of the pyramid
	glm::vec3 planePositions[] =
	{
		glm::vec3(0.0f, 0.0f, 0.5f),
		glm::vec3(0.5f, 0.0f, 0.0f),
		glm::vec3(0.0f, 0.0f, -0.5f),
		glm::vec3(-0.5f, 0.0f, 0.0f),

	};
	//Plane Rotations: The  plane rotations are used to help rotate the pyramid 
	//to any locations you choose.
	glm::float32 planeRotationsY[] =
	{
		0.0f, 90.0f, 180.0f, -90.0f, -90.0f, 90.0f
	};
	glm::float32 planeRotationsX[] =
	{
		-30.0f, -30.0f, -30.0f, -30.0f, 30.0
	};
	//Enable Depth Buffer
	glEnable(GL_DEPTH_TEST);

	//WireFrame Mode: This statement is only to
	//be used if you want to see the skeleton structure of the pyramid
	//glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
	//These statements will help to test the vertices of the pyramid and the 
	//lamp of the camera. This variables must need to c
	GLuint pyramidVBO, pyramidEBO, pyramidVAO, lampVBO, lampEBO, lampVAO;
	//Create VBO for the pyramid
	glGenBuffers(1, &pyramidVBO);
	//Create EBO for the pyramid
	glGenBuffers(1, &pyramidEBO);

	//Create VOA
	glGenVertexArrays(1, &pyramidVAO);

	//Create VBO for the lamp
	glGenBuffers(1, &lampVBO);
	//Create EBO for the lamp
	glGenBuffers(1, &lampEBO);

	//Create VAO for the lamp
	glGenVertexArrays(1, &lampVAO);
	//Create VAO for the pyramid
	glBindVertexArray(pyramidVAO);

	//VBO and EBO Placed in User-Defined VAO
	//SELECT VBO
	glBindBuffer(GL_ARRAY_BUFFER, pyramidVBO);
	//SELECT EBO
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, pyramidEBO);

	// Load vertex attributes
	glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

	// Load indices
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);

	// Specify attribute location and layout to GPU
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 11 * sizeof(GLfloat), (GLvoid*)0);
	glEnableVertexAttribArray(0);

	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 11 * sizeof(GLfloat), (GLvoid*)(3 * sizeof(GLfloat)));
	glEnableVertexAttribArray(1);

	glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 11 * sizeof(GLfloat), (GLvoid*)(6 * sizeof(GLfloat)));
	glEnableVertexAttribArray(2);

	glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, 11 * sizeof(GLfloat), (GLvoid*)(8 * sizeof(GLfloat)));
	glEnableVertexAttribArray(3);
	glBindVertexArray(0);


	// Define lamp VAO
	glBindVertexArray(lampVAO);
	//Select VBO
	glBindBuffer(GL_ARRAY_BUFFER, lampVBO);
	//Select VBO
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, lampEBO);
	// Load vertex attributes
	glBufferData(GL_ARRAY_BUFFER, sizeof(lampVertices), lampVertices, GL_STATIC_DRAW);
	// Load indices
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0 * sizeof(GLfloat), (GLvoid*)0);
	glEnableVertexAttribArray(0);

	// Unbind VOA or close off (Must call VOA explicitly in loop)
	glBindVertexArray(0);

	//Load textures
	int pyramidTexWidth, pyramidTexHeight;
	unsigned char* pyramidImage = SOIL_load_image("pyramid.jpg", &pyramidTexWidth,
		&pyramidTexHeight, 0, SOIL_LOAD_RGB);

	// Generate Textures
	GLuint pyramidTexture;
	glGenTextures(1, &pyramidTexture);
	glBindTexture(GL_TEXTURE_2D, pyramidTexture);
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, pyramidTexWidth, pyramidTexHeight, 0,
		GL_RGB, GL_UNSIGNED_BYTE, pyramidImage);

	glGenerateMipmap(GL_TEXTURE_2D);
	SOIL_free_image_data(pyramidImage);
	glBindTexture(GL_TEXTURE_2D, 0);

	//Vertex shader source code
	string vertexShaderSource =
		"#version 330 core\n"
		"layout(location = 0) in vec3 vPosition;"
		"layout(location = 1) in vec3 aColor;"
		"layout(location = 2) in vec2 texCoord;"
		"layout(location = 3) in vec3 normal;"
		"out vec3 oColor;"
		"out vec2 oTexCoord;"
		"out vec3 oNormal;"
		"out vec3 FragPos;"
		"uniform mat4 model;"
		"uniform mat4 view;"
		"uniform mat4 projection;"
		"void main()\n"
		"{\n"
		"gl_Position = projection * view * model *vec4(vPosition.x,  vPosition.y,  vPosition.z, 1.0);"
		"oColor = aColor;"
		"oTexCoord = texCoord;"
		"oNormal = mat3(transpose(inverse(model))) * normal;"
		"FragPos = vec3(model * vec4(vPosition, 1.0f));"
		"}\n";

	//Fragment shader source code
	string fragmentShaderSource =
		"#version 330 core\n"
		"in vec3 oColor;"
		"in vec2 oTexCoord;"
		"in vec3 oNormal;"
		"in vec3 FragPos;"
		"out vec4 fragColor;"
		"uniform sampler2D myTexture;"
		"uniform vec3 objectColor;"
		"uniform vec3 lightColor;"
		"uniform vec3 lightPos;"
		"uniform vec3 lightPos2;"
		"uniform vec3 viewPos;"
		"uniform vec3 viewPos2;"
		"void main()\n"
		"{\n"
		"//Ambient\n"
		"float ambientStrength = 0.1f;"
		"vec3 ambient = ambientStrength * lightColor;"
		"//Disffuse\n"
		"vec3 norm = normalize(oNormal);"
		"vec3 lightDir = normalize(lightPos - FragPos);"
		"float diff = max(dot(norm, lightDir), 1.0);"
		"vec3 diffuse = diff * lightColor;"
		"//Specularity\n"
		"float specularStrength = 3.0f;"
		"vec3 viewDir = normalize(viewPos - FragPos);"
		"vec3 reflectDir = reflect(-lightDir, norm);"
		"float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);"
		"vec3 specular = specularStrength * spec * lightColor;"
		"vec3 result = (ambient + diffuse + specular) * objectColor;"
		"fragColor = texture(myTexture, oTexCoord) * vec4(result, 1.0f);"
		"}\n";

	//Lamp Vertex shader source code
	string lampVertexShaderSource =
		"#version 330 core\n"
		"layout(location = 0) in vec3 vPosition;"
		"uniform mat4 model;"
		"uniform mat4 view;"
		"uniform mat4 projection;"
		"void main()\n"
		"{\n"
		"gl_Position = projection * view * model *vec4(vPosition.x,  vPosition.y,  vPosition.z, 1.0);"
		"}\n";

	// Lamp Fragment shader source code
	string lampFragmentShaderSource =
		"#version 330 core\n"
		"out vec4 fragColor;"
		"uniform vec3 lightColor;"
		"void main()\n"
		"{\n"
		"fragColor = vec4(1.0f);"
		"}\n";
	//Creating Shader Program
	GLuint shaderProgram = CreateShaderProgram(vertexShaderSource, fragmentShaderSource);
	GLuint lampShaderProgram = CreateShaderProgram(lampVertexShaderSource, lampFragmentShaderSource);

	/*The while loop will help the user to loop around the window from moving the window any
	  directions they want the window to appear until the user decided it is time
	  to close the window then it will automatically exit the user from using the window.
	  Once the user closes the window from using the x in the upper right corner of the window.*/
	while (!glfwWindowShouldClose(window))
	{
		//Set delta time
		GLfloat currentFrame = glfwGetTime();
		deltaTime = currentFrame - lastFrame;
		lastFrame = currentFrame;

		//This method will buffering the frame of the size of the shape. 
		//From letting it to have a even size to the window format.
		glfwGetFramebufferSize(window, &width, &height);

		//This method will keep the size from moving into a different direction 
		//for to let the width and hight of the shape to stay in the same direction.
		glViewport(0, 0, width, height);

		/*The glClear method will help the window to buffer and creates the
		color of the window context from rendering it to the application.*/
		//This method will use the buffering color and it will set the color to use for the shape. 
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
		// Use Shader Program exe.
		glUseProgram(shaderProgram);
		//The statement will add a background color
		//to the window of the back of the Pyramid
		glClearColor(1.0f, 0.0f, 0.0f, 0.0f);

		//Declare identity matrix 
		glm::mat4 projectionMatrix;

		//Initialize transforms
		viewMatrix = glm::lookAt(cameraPosition, getTarget(), worldUp);

		//Initialize the height and width of the projector 
		projectionMatrix = glm::perspective(fov, (GLfloat)width / (GLfloat)height, 0.1f, 100.0f);

		//Select uniform shader and variable
		GLint modelLoc = glGetUniformLocation(shaderProgram, "model");
		GLint viewLoc = glGetUniformLocation(shaderProgram, "view");
		GLint projectionLoc = glGetUniformLocation(shaderProgram, "projection");

		//Get light and object color and light position location
		GLint objectColorLoc = glGetUniformLocation(shaderProgram, "objectColor");
		GLint lightColorLoc = glGetUniformLocation(shaderProgram, "lightColor");
		GLint lightPosLoc = glGetUniformLocation(shaderProgram, "lightPos");

		GLint viewPosLoc = glGetUniformLocation(shaderProgram, "viewPos");

		//Assign Light and Object Colors 
		//Also, it will change the pyramid to a orange color
		glUniform3f(objectColorLoc, 1.0f, 0.5f, 0.0f);
		glUniform3f(lightColorLoc, 1.0f, 1.0f, 1.0f);

		//Set light position
		glUniform3f(lightPosLoc, lightPosition.x, lightPosition.y, lightPosition.z);

		//Specify view position
		glUniform3f(viewPosLoc, cameraPosition.x, cameraPosition.y, cameraPosition.z);

		//Pass transform to Shader
		glUniformMatrix4fv(viewLoc, 1, GL_FALSE, glm::value_ptr(viewMatrix));
		glUniformMatrix4fv(projectionLoc, 1, GL_FALSE, glm::value_ptr(projectionMatrix));

		glBindTexture(GL_TEXTURE_2D, pyramidTexture);

		// User-defined VAO must be called before draw
		glBindVertexArray(pyramidVAO);

		for (GLuint i = 0; i < 4; i++)
		{
			glm::mat4 modelMatrix;
			modelMatrix = glm::translate(modelMatrix, planePositions[i]);
			modelMatrix = glm::rotate(modelMatrix, planeRotationsY[i] * toRadians, glm::vec3(0.0f, 1.0f, 0.0f));
			modelMatrix = glm::rotate(modelMatrix, planeRotationsX[i] * toRadians, glm::vec3(1.0f, 0.0f, 0.0f));

			//Selecing the model matrix
			glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm::value_ptr(modelMatrix));

			//Drawing the triangle of the pyramid shape
			draw();
		};
		//Incase different VAO will be used after
		glBindVertexArray(0);
		
		//Using the lamp Shader Program
		glUseProgram(lampShaderProgram);

		//Select uniform shader and variable
		GLint lampModelLoc = glGetUniformLocation(lampShaderProgram, "model");
		GLint lampModelLoc2 = glGetUniformLocation(lampShaderProgram, "model");

		GLint lampViewLoc = glGetUniformLocation(lampShaderProgram, "view");
		GLint lampProjectionLoc = glGetUniformLocation(lampShaderProgram, "projection");
		GLint lampProjectionLoc2 = glGetUniformLocation(lampShaderProgram, "projection");

		glUniformMatrix4fv(lampViewLoc, 1, GL_FALSE, glm::value_ptr(viewMatrix));
		glUniformMatrix4fv(lampProjectionLoc, 1, GL_FALSE, glm::value_ptr(projectionMatrix));

		// User-defined VAO must be called before draw
		glBindVertexArray(lampVAO);

		for (GLuint i = 0; i < 4; i++)
		{
			glm::mat4 modelMatrix;
			//Translating the positions of the light and rotating it to poistion the light location
			modelMatrix = glm::translate(modelMatrix, planePositions[i] / glm::vec3(8., 8., 8.) + lightPosition);
			modelMatrix = glm::rotate(modelMatrix, planeRotationsY[i] * toRadians, glm::vec3(0.0f, 1.0f, 0.0f));
			modelMatrix = glm::scale(modelMatrix, glm::vec3(.125f, .125f, .125f));
			modelMatrix = glm::rotate(modelMatrix, planeRotationsX[i] * toRadians, glm::vec3(1.0f, 0.0f, 0.0f));
			glUniformMatrix4fv(lampModelLoc, 1, GL_FALSE, glm::value_ptr(modelMatrix));

			//Drawing the triangle for light pyramid of the lightbulb 
			draw();
		}
		glBindVertexArray(0);
		// Incase different shader will be used after
		/*From using the glfwSwapBuffers it
		let's the user to move any direction front or back when increasing the size of the window.*/
		glUseProgram(0);
		glfwSwapBuffers(window);

		/*From using the glfwPollEvents it will update and processing the rendering method to
		let the window to resize any size does the user want to resize it at.*/
		glfwPollEvents();

		//Poll camera transformations
		TransformCamera();
	};
};
//Define Input Callback functions
void key_callback(GLFWwindow * window, int key, int scancode, int action, int mods)
{
	//Define ASCII Keycode
	//cout << "ASCII: " << key << endl;

	if (action == GLFW_PRESS)
		keys[key] = true;
	else
		if (action == GLFW_RELEASE)
			keys[key] = false;
}

void scroll_callback(GLFWwindow * window, double xoffset, double yoffset)
{

	//Clamp FOV the clamp fov will let the design to move only in the center
	//of the window but when you click on the right button of the mouse
	//it will let the design to move anywhere you want it to go.
	if (fov >= 1.f && fov <= 45.f)
		fov -= yoffset * 0.01f;

	//Default FOV
	if (fov < 1.f)
		fov = 1.f;
	if (fov > 45.f)
		fov = 45.f;
}

void cursor_position_callback(GLFWwindow * window, double xpos, double ypos)
{
	//Display Mouse X and Y Coordinates
	//cout << "Mouse X: " << xpos << endl;
	//cout << "Mouse Y: " << ypos << endl;

	if (firstMouseMove)
	{
		lastX = xpos;
		lastY = ypos;
		firstMouseMove = false;
	}

	//Calculate cursor offset
	xChange = xpos - lastX;
	yChange = lastY - ypos;

	lastX = xpos;
	lastY = ypos;

	//Pan camera
	if (isPanning)
	{
		if (cameraPosition.z < 0.f)
			cameraFront.z = 1.f;
		else
			cameraFront.z = -1.f;
		GLfloat cameraSpeed = xChange * deltaTime;
		cameraPosition += cameraSpeed * cameraRight;

		cameraSpeed = yChange * deltaTime;
		cameraPosition += cameraSpeed * cameraUp;
	}

	//Orbit camera
	if (isOrbiting)
	{
		rawYaw += xChange;
		rawPitch += yChange;

		// Convert Yaw and Pitch to degrees
		degYaw = glm::radians(rawYaw);
		//degPitch = glm::radians(rawPitch);
		degPitch = glm::clamp(glm::radians(rawPitch), -glm::pi<float>() / 2.f + .1f, glm::pi<float>() / 2.f - .1f);


		// Azimuth Altitude formula
		cameraPosition.x = target.x + radius * cosf(degPitch) * sinf(degYaw);
		cameraPosition.y = target.y + radius * sinf(degPitch);
		cameraPosition.z = target.z + radius * cosf(degPitch) * cosf(degYaw);
	}
}
//This statement will help to let you use the buttons of your mouse to move 
//the object to any location you prefere and it will callback the buttons of 
//which button was pressed to move the object in any directions you prefere. 
void mouse_button_callback(GLFWwindow * window, int button, int action, int mods)
{
	if (action == GLFW_PRESS)
		mouseButtons[button] = true;
	else
		if (action == GLFW_RELEASE)
			mouseButtons[button] = false;

}

//Define getTarget function
glm::vec3 getTarget()
{
	if (isPanning)
		target = cameraPosition + cameraFront;

	return target;
}
//Define TransformCamera function
void TransformCamera()
{
	// Pan camera
	if (keys[GLFW_KEY_LEFT_ALT] && mouseButtons[GLFW_MOUSE_BUTTON_MIDDLE])
		isPanning = true;
	else
		isPanning = false;

	if (keys[GLFW_KEY_LEFT_ALT] && mouseButtons[GLFW_MOUSE_BUTTON_RIGHT])
		isPanning = true;
	else
		isPanning = false;

	//Orbit camera 
	if (keys[GLFW_KEY_LEFT_ALT] && mouseButtons[GLFW_MOUSE_BUTTON_LEFT])
		isOrbiting = true;
	else
		isOrbiting = false;
	//Reset camera
	if (keys[GLFW_KEY_F])
		initCamera();
}
//The void initCamera will adjust the structure of the design location.
void initCamera()
{
	cameraPosition = glm::vec3(0.f, 0.f, 3.f);
	target = glm::vec3(0.f, 0.f, 0.f);
	cameraDirection = glm::normalize(cameraPosition - target);
	worldUp = glm::vec3(0.f, 1.f, 0.f);
	cameraRight = glm::normalize(glm::cross(worldUp, cameraDirection));
	cameraUp = glm::normalize(glm::cross(cameraDirection, cameraRight));
	cameraFront = glm::normalize(glm::vec3(0.f, 0.f, -1.f));
}