#include "config.hpp"
#include "Intersection.hpp"
#include <cassert>
#include <algorithm>
#include <cstdlib>
#include <iostream>
using namespace std;




Direction::Direction(const string& name, int lanes_num):_name(name), _lanes_num(lanes_num), _q_length_list(lanes_num, 0){
}

int Direction::getQLength() const {
    if (0 == _lanes_num){
        return 0;
    }
    return _q_length_list[0];
    //return (*max_element(_q_length_list.begin(),_q_length_list.end()));
}

void Direction::updateQLengthList() {
	if(0 == _lanes_num)
		return;
	_q_length_list[0] = singleton.multientryexit.getLastStepVehicleNumber(_name);
    // for(int i = 0; i < _lanes_num; ++i){
    //     string sensor_name = _name + to_string(i);
    //     _q_length_list[i] = singleton.lane.getLastStepVehicleNumber(sensor_name);
    // }
}

Intersection::Intersection(const string& name):_name(name), west(nullptr), east(nullptr), north(nullptr), south(nullptr){
}

void Intersection::setLight(int min, int max){
	lightMin = min;
	lightMax = max;
}

void Intersection::setLightEncode(const string& nsG, const string& weG){
	nsGreen = nsG;
	weGreen = weG;
}

string Intersection::getLightState(){
	return singleton.trafficlights.getRedYellowGreenState(_name);
}

void Intersection::setLightState(const string& ltState){
	singleton.trafficlights.setRedYellowGreenState(_name, ltState);
}

void Intersection::setLines(int west_lanes_num, int east_lanes_num, int north_lanes_num, int south_lanes_num){
	west = new Direction(_name + "W", west_lanes_num);
	east = new Direction(_name + "E", east_lanes_num);
	north = new Direction(_name + "N", north_lanes_num);
	south = new Direction(_name + "S", south_lanes_num);
}

void Intersection::setThreshold(int we, int ns){
	weThreshold = we;
	nsThreshold = ns;
}

void Intersection::loadFromData(const map<string, vector<string>>& dataDict){
	vector<string> dataList = dataDict.at(_name);
	assert(6 == dataList.size());
	setLightEncode(dataList[0], dataList[1]);
	setLines(stoi(dataList[2]), stoi(dataList[3]), stoi(dataList[4]), stoi(dataList[5]));
}

void Intersection::updateQLength(){
	west->updateQLengthList();
	east->updateQLengthList();
	north->updateQLengthList();
	south->updateQLengthList();
	nsQLength = north->getQLength() + south->getQLength();
	weQLength = west->getQLength() + east->getQLength();
}

void Intersection::updateClock(){
	if(lightState == nsGreen){
		++nsClock;
		weClock = 0;
	}else if(lightState == weGreen){
		++weClock;
		nsClock = 0;
	}

}

void Intersection::init(){
	lightMax = 1200;
	lightMin = 300;
	defaultInterval = 900;

	weClock = 0;
	weQLength = 0;

	nsClock = 0;
	nsQLength = 0;
	lightState = getLightState();
	assert(lightState == nsGreen || lightState == weGreen);
}

void Intersection::changeLight(){
	if(nsGreen == lightState){
		setLightState(weGreen);
		lightState = weGreen;
	}else if(weGreen == lightState){
		setLightState(nsGreen);
		lightState = nsGreen;
	}
}

void Intersection::keepLight(){
	setLightState(lightState);
}

void Intersection::controllor(){
	if(((weQLength < weThreshold && nsQLength < nsThreshold) ||	(weQLength >= weThreshold && nsQLength >= nsThreshold))
			&& (weClock > lightMax || nsClock > lightMax)){
		changeLight();
	}else if((weQLength >= weThreshold && nsQLength < nsThreshold)
			&&(nsClock > lightMin || weClock > lightMax)){
		changeLight();
	}else if((nsQLength >= nsThreshold && weQLength < weThreshold)
			&&(weClock > lightMin || nsClock > lightMax)){
		changeLight();
	}else
		keepLight();
}

void Intersection::defaultControllor(){
	if(weClock > defaultInterval || nsClock > defaultInterval)
		changeLight();
}

void Intersection::defaultRun(){
	defaultControllor();
	updateClock();
	assert(lightState == nsGreen || lightState == weGreen);
}

void Intersection::run(){
	if(0 == nsThreshold && 0 == weThreshold){
		defaultControllor();
		updateClock();
	}else{
		updateQLength();
		controllor();
		updateClock();
	}

	assert (lightState == nsGreen || lightState == weGreen);
}

void Intersection::debug(){
	return;
}

Intersection::~Intersection(){
	assert (nullptr != west);
	assert (nullptr != east);
	assert (nullptr != north);
	assert (nullptr != south);
	delete west;
	delete east;
	delete north;
	delete south;
}

