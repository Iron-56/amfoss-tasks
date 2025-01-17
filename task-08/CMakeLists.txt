cmake_minimum_required(VERSION 3.10)
project(VulkanGLFWExample)

# Find Vulkan and GLFW
find_package(Vulkan REQUIRED)
find_package(glfw3 REQUIRED)

# Set up the executable
add_executable(VulkanGLFWExample main.cpp)

# Link Vulkan and GLFW
target_link_libraries(VulkanGLFWExample PRIVATE Vulkan::Vulkan glfw)
