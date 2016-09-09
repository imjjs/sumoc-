//
// Created by yli on 3/14/2016.
//

#ifndef CONTROLLOR_INTERSECTION_HPP
#define CONTROLLOR_INTERSECTION_HPP

#include <string>
#include <vector>
#include "config.hpp"
#include <map>



class Direction {
private:
    std::string _name;
    int _lanes_num;
    std::vector<int> _q_length_list;
public:
    Direction(const std::string& name, int lanes_num);
    virtual ~Direction(){}
    int getQLength()const;
    void updateQLengthList();
};
class Intersection {
private:
	std::string _name;
	std::string lightState;
	int lightMax;
	int lightMin;
	int defaultInterval;

	int weClock;
	int weQLength;
	std::string weGreen;
	int weThreshold;

	int nsClock;
	int nsQLength;
	std::string nsGreen;
	int nsThreshold;

	Direction* north;
	Direction* south;
	Direction* west;
	Direction* east;

public:
	Intersection(const std::string& name);
	virtual ~Intersection();
	void setLight(int min, int max);
	void setLightEncode(const std::string& nsG, const std::string& weG);
	std::string getLightState();
	void setLightState(const std::string& ltState);
	void setLines(int west_lanes_num, int east_lanes_num, int north_lanes_num, int south_lanes_num);
	void setThreshold(int we, int ns);
	void loadFromData(const std::map<std::string, std::vector<std::string>>& dict);
	void updateQLength();
	void updateClock();
	void init();
	void changeLight();
	void keepLight();
	void controllor();
	void defaultControllor();
	void defaultRun();
	void run();
	void debug();

};


#endif //CONTROLLOR_INTERSECTION_HPP
