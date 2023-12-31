#ifndef GENERIC_DISPLAY_H
#define GENERIC_DISPLAY_H

#include <sl/Fusion.hpp>
#include "GLViewer.hpp"

class GenericDisplay
{
public:
/**
 * @brief Construct a new Generic Display object
 * 
 */
    GenericDisplay();
    /**
     * @brief Destroy the Generic Display object
     * 
     */
    ~GenericDisplay();
    /**
     * @brief Init OpenGL display with the requested camera_model (used as moving element in OpenGL view)
     * 
     * @param argc default main argc
     * @param argv default main argv
     * @param camera_model zed camera model to use
     */
    void init(int argc, char **argv);
    /**
     * @brief Return if the OpenGL viewer is still open
     * 
     * @return true the OpenGL viewer is still open
     * @return false the OpenGL viewer was closed
     */
    bool isAvailable();
    /**
     * @brief Update the OpenGL view with last pose data
     * 
     * @param zed_rt last pose data
     * @param state current tracking state
     */
    void updatePoseData(sl::Transform zed_rt, sl::POSITIONAL_TRACKING_STATE state);
    /**
     * @brief Display current fused pose either in KML file or in ZEDHub depending compilation options
     * 
     * @param geo_pose geopose to display
     * @param current_timestamp timestamp of the geopose to display
     */
    void updateGeoPoseData(sl::GeoPose geo_pose, sl::Timestamp current_timestamp);

protected:
    GLViewer opengl_viewer;
};

#endif