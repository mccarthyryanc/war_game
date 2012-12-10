%
% matlab script to analyze warGame data
%
%

%Plot of filled Phase Space
%cards = [1 1 1 1 2 2 2 2 3 3 3 3 4 4 4 4 5 5 5 5 6 6 6 6 7 7 7 7 8 8 8 8 9 9 9 9 10 10 10 10 11 11 11 11 12 12 12 12 13 13 13 13 14 14 14 14];
%x = linspace(0,420);
%y = 420 - x;

% 
% ------METHOD 1------
% One Dimensional parameter is the angle formed by the sum of each players hand, if player one's sum is a length, x, and player two's sum is a length, y.
%		theta = arctan(y/x) - pi/4
%	shifted by pi/4 so a negative value meams that player 1 is winning and positive value means that player two is winning.
%
% ------METHOD 2------
% Simply Measure the "angle" between each player's hand, where each hand is treated as a 52 element vector:
%     theta = arccos(p1*p2/(|p1|*|p2|))
%
%
%

%change to the correct directory
dirct = '/home/ryans/Documents/wargame';
datadirct = [dirct, '/trials'];

%cycle game variable
cycgame = 0;

%loop through
for i = 500:600
	filename = [datadirct,'/trial_',num2str(i),'.csv'];
	
	%import data
	data = importdata(filename, ' ');
	siz = size(data);
	%check if the game made it to maxIter defined in simpleWarGame.py (default was 8000).
	if sum(data(end,:) == 9999) == 1
		display(['Possible cycle game at trial ', num2str(i)]);
		siz(1) = siz(1) - 1;
		data = data(1:end-1,:);
		cycgame = 1
	end
	
	%easy reference to each players hand	
	p1 = data([1:2:siz(1)],:);
	p2 = data([2:2:siz(1)],:);
	
	theta1 = zeros(siz(1)/2,1);
	theta2 = zeros(siz(1)/2,1);
	theta = zeros(siz(1)/2,1);
	
	%loop through a game and determine the theta
	for j = 1:(siz(1)/2)
		%METHOD 1
		theta1(j) = atan2(sum(p2(j,:)),sum(p1(j,:))) - pi/4;
		
		%METHOD 2 with a shift
		theta2(j) = acos((p1(j,:)*p2(j,:)')/(norm(p1(j,:))*norm(p2(j,:)))) - pi/4;
		
		%add the two methods
		theta(j) = theta1(j) + theta2(j);
		
	end 
	
	%plot and save the data
	if cycgame
		temp = ['Trial_', num2str(i)];
		titletext = {temp, 'Possible Cycle'};
	else
		titletext = ['Trial', num2str(i)];
	end
	
	h1 = figure('visible','off');
	hold on
	plot(theta1, 'b')
	plot(theta2, 'r')
	plot(theta, 'g')
	title(titletext, 'FontSize',16);
	xlabel('Iterations through Single Game','FontSize',12);
	ylabel('Theta','FontSize',12);
	legend('\theta_1','\theta_2', '\theta_1 + \theta_2', 'Location', 'NorthWest')
	set(h1, 'Position', [100,100,900,700]);
	saveas(h1,[dirct,'/figures/trial_',num2str(i)],'png');
	
end	
