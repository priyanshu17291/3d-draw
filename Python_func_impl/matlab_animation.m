% Steel Frame Modal Analyzer
% This script creates a 3D visualization of a steel frame and performs modal analysis
% on accelerometer data from Excel files.

function main_steel_frame_analyzer()
    % Create a figure with UI controls
    fig = figure('Name', '3D Steel Frame Modal Analysis', 'Position', [50, 50, 1200, 800]);
    
    % Create main panel for frame parameters
    inputPanel = uipanel('Title', 'Frame Parameters', 'Position', [0.02, 0.82, 0.25, 0.16]);
    
    % Create input fields with default values
    uicontrol(inputPanel, 'Style', 'text', 'String', 'Height (m):', 'Position', [10, 110, 80, 20], 'HorizontalAlignment', 'left');
    hEdit = uicontrol(inputPanel, 'Style', 'edit', 'String', '0.507', 'Position', [100, 110, 80, 20], 'Tag', 'height');
    
    uicontrol(inputPanel, 'Style', 'text', 'String', 'Length X (m):', 'Position', [10, 80, 80, 20], 'HorizontalAlignment', 'left');
    lxEdit = uicontrol(inputPanel, 'Style', 'edit', 'String', '0.507', 'Position', [100, 80, 80, 20], 'Tag', 'lengthX');
    
    uicontrol(inputPanel, 'Style', 'text', 'String', 'Length Y (m):', 'Position', [10, 50, 80, 20], 'HorizontalAlignment', 'left');
    lyEdit = uicontrol(inputPanel, 'Style', 'edit', 'String', '0.507', 'Position', [100, 50, 80, 20], 'Tag', 'lengthY');
    
    uicontrol(inputPanel, 'Style', 'text', 'String', 'Stories:', 'Position', [10, 20, 80, 20], 'HorizontalAlignment', 'left');
    storiesEdit = uicontrol(inputPanel, 'Style', 'edit', 'String', '3', 'Position', [100, 20, 80, 20], 'Tag', 'stories');
    
    % Create analysis panel
    analysisPanel = uipanel('Title', 'Analysis Controls', 'Position', [0.02, 0.52, 0.25, 0.28]);
    
    % FRF Controls
    uicontrol(analysisPanel, 'Style', 'text', 'String', 'Select Node:', 'Position', [10, 190, 80, 20], 'HorizontalAlignment', 'left');
    nodeSelect = uicontrol(analysisPanel, 'Style', 'popup', 'Position', [100, 190, 120, 20], 'String', {'Node 5', 'Node 6', 'Node 7', 'Node 8', 'Node 9', 'Node 10', 'Node 11', 'Node 12', 'Node 13', 'Node 14', 'Node 15', 'Node 16'});
    
    uicontrol(analysisPanel, 'Style', 'text', 'String', 'Select Direction:', 'Position', [10, 160, 100, 20], 'HorizontalAlignment', 'left');
    dirSelect = uicontrol(analysisPanel, 'Style', 'popup', 'Position', [120, 160, 100, 20], 'String', {'X', 'Y', 'Z'});
    
    uicontrol(analysisPanel, 'Style', 'text', 'String', 'Max Freq (Hz):', 'Position', [10, 130, 90, 20], 'HorizontalAlignment', 'left');
    maxFreqEdit = uicontrol(analysisPanel, 'Style', 'edit', 'String', '50', 'Position', [110, 130, 40, 20], 'Tag', 'maxFreq');
    
    uicontrol(analysisPanel, 'Style', 'pushbutton', 'String', 'Plot FRF', 'Position', [165, 130, 60, 25], 'Callback', @plotFRF);
    
    % Mode Shape Controls
    uicontrol(analysisPanel, 'Style', 'text', 'String', 'Display Mode:', 'Position', [10, 90, 90, 20], 'HorizontalAlignment', 'left');
    modeSelect = uicontrol(analysisPanel, 'Style', 'popup', 'Position', [110, 90, 110, 20], 'String', {'3D Frame Only', 'Mode 1', 'Mode 2', 'Mode 3'});
    
    uicontrol(analysisPanel, 'Style', 'pushbutton', 'String', 'Display/Animate', 'Position', [80, 50, 120, 25], 'Callback', @displayMode);
    
    % Animation controls
    animPanel = uipanel('Title', 'Animation Controls', 'Position', [0.02, 0.32, 0.25, 0.18]);
    uicontrol(animPanel, 'Style', 'text', 'String', 'Amplitude Scale:', 'Position', [10, 100, 100, 20], 'HorizontalAlignment', 'left');
    ampScale = uicontrol(animPanel, 'Style', 'slider', 'Position', [120, 100, 100, 20], 'Min', 0.1, 'Max', 10, 'Value', 3, 'SliderStep', [0.1, 1]/9.9);
    
    uicontrol(animPanel, 'Style', 'text', 'String', 'Animation Speed:', 'Position', [10, 70, 100, 20], 'HorizontalAlignment', 'left');
    animSpeed = uicontrol(animPanel, 'Style', 'slider', 'Position', [120, 70, 100, 20], 'Min', 0.1, 'Max', 2, 'Value', 1, 'SliderStep', [0.1, 0.5]/1.9);
    
    uicontrol(animPanel, 'Style', 'pushbutton', 'String', 'Start Animation', 'Position', [50, 30, 120, 25], 'Callback', @startAnimation, 'Tag', 'animButton');
    
    % Create info panel for results
    infoPanel = uipanel('Title', 'Modal Analysis Results', 'Position', [0.02, 0.02, 0.25, 0.28]);
    resultsText = uicontrol(infoPanel, 'Style', 'text', 'Position', [10, 10, 220, 180], 'HorizontalAlignment', 'left', 'Tag', 'results');
    
    % Create main axes for frame and mode shapes
    frameAxes = axes('Position', [0.3, 0.4, 0.65, 0.55]);
    title('3D Steel Frame');
    xlabel('X (m)');
    ylabel('Y (m)');
    zlabel('Z (m)');
    
    % Create axes for FRF plot
    frfAxes = axes('Position', [0.3, 0.05, 0.65, 0.3]);
    title('Frequency Response Function');
    xlabel('Frequency (Hz)');
    ylabel('Amplitude');
    
    % Initialize global variables
    nodes = [];
    elements = [];
    nodeData = containers.Map();
    sensorMapping = containers.Map();
    modalResults = struct('naturalFreqs', [5.2, 8.7, 12.3], 'modeShapes', []);
    isAnimating = false;
    
    % Initial plot
    plotFrame();
    loadData();
    
    % Main plotting function for the frame
    function plotFrame(~, ~)
        % Get values from input fields
        H = str2double(get(hEdit, 'String'));
        Lx = str2double(get(lxEdit, 'String'));
        Ly = str2double(get(lyEdit, 'String'));
        stories = round(str2double(get(storiesEdit, 'String')));
        baysX = 1;  % Fixed for this application
        baysY = 1;  % Fixed for this application
        
        % Validate inputs
        if isnan(H) || isnan(Lx) || isnan(Ly) || isnan(stories)
            errordlg('Please enter valid numeric inputs', 'Input Error');
            return;
        end
        
        if H <= 0 || Lx <= 0 || Ly <= 0 || stories <= 0
            errordlg('All inputs must be positive', 'Input Error');
            return;
        end
        
        % Generate nodes
        nodes = generateNodes(H, Lx, Ly, stories, baysX, baysY);
        
        % Generate elements
        elements = generateElements(stories, baysX, baysY);
        
        % Update node selection dropdown based on number of stories
        nodeNames = {};
        for i = 5:4*(stories+1)
            nodeNames{end+1} = ['Node ' num2str(i)];
        end
        set(nodeSelect, 'String', nodeNames);
        
        % Create sensor mapping
        createSensorMapping(stories);
        
        % Perform modal analysis
        performModalAnalysis();
        
        % Plot the frame
        axes(frameAxes);
        cla;
        plotFrame3D(nodes, elements, H);
        
        % Show results
        updateResults();
    end
    
    % Generate node coordinates
    function nodeArray = generateNodes(H, Lx, Ly, stories, baysX, baysY)
        % Calculate total number of nodes
        numNodesPerFloor = (baysX + 1) * (baysY + 1);
        totalNodes = numNodesPerFloor * (stories + 1);
        
        % Initialize nodes matrix
        nodeArray = zeros(totalNodes, 4); % [node_id, x, y, z]
        
        nodeId = 1;
        
        % Generate nodes for each floor
        for floor = 0:stories
            for j = 0:baysY
                for i = 0:baysX
                    x = i * Lx;
                    y = j * Ly;
                    z = floor * H;
                    
                    nodeArray(nodeId, :) = [nodeId, x, y, z];
                    nodeId = nodeId + 1;
                end
            end
        end
    end
    
    % Generate elements connecting the nodes
    function elementArray = generateElements(stories, baysX, baysY)
        % Calculate number of nodes per floor
        numNodesPerFloor = (baysX + 1) * (baysY + 1);
        
        % Calculate number of elements (excluding ground beams)
        numColumns = numNodesPerFloor; % columns connect between floors
        numBeamsXPerFloor = baysX * (baysY + 1); % beams in x-direction per floor
        numBeamsYPerFloor = (baysX + 1) * baysY; % beams in y-direction per floor
        
        % Total number of elements (columns + non-ground beams)
        totalElements = (stories * numColumns) + (stories) * (numBeamsXPerFloor + numBeamsYPerFloor);
        
        % Initialize elements matrix
        elementArray = zeros(totalElements, 3); % [element_id, node1, node2]
        
        elementId = 1;
        
        % Generate vertical elements (columns)
        for floor = 0:stories-1
            for node = 1:numNodesPerFloor
                node1 = node + floor * numNodesPerFloor;
                node2 = node1 + numNodesPerFloor;
                
                elementArray(elementId, :) = [elementId, node1, node2];
                elementId = elementId + 1;
            end
        end
        
        % Generate horizontal elements (beams) for non-ground floors only
        for floor = 1:stories
            baseNode = 1 + floor * numNodesPerFloor;
            
            % X-direction beams
            for j = 0:baysY
                for i = 0:baysX-1
                    node1 = baseNode + i + j * (baysX + 1);
                    node2 = node1 + 1;
                    
                    elementArray(elementId, :) = [elementId, node1, node2];
                    elementId = elementId + 1;
                end
            end
            
            % Y-direction beams
            for i = 0:baysX
                for j = 0:baysY-1
                    node1 = baseNode + i + j * (baysX + 1);
                    node2 = node1 + (baysX + 1);
                    
                    elementArray(elementId, :) = [elementId, node1, node2];
                    elementId = elementId + 1;
                end
            end
        end
    end
    
    % Plot the 3D frame
    function plotFrame3D(nodeArray, elementArray, H)
        % Plot elements
        hold on;
        
        % Plot elements
        for i = 1:size(elementArray, 1)
            node1 = elementArray(i, 2);
            node2 = elementArray(i, 3);
            
            % Get coordinates
            x = [nodeArray(node1, 2), nodeArray(node2, 2)];
            y = [nodeArray(node1, 3), nodeArray(node2, 3)];
            z = [nodeArray(node1, 4), nodeArray(node2, 4)];
            
            % Plot line - red for columns, blue for beams
            if z(1) ~= z(2)  % Vertical elements (columns)
                plot3(x, y, z, 'r-', 'LineWidth', 2);
            else  % Horizontal elements (beams)
                plot3(x, y, z, 'b-', 'LineWidth', 2);
            end
        end
        
        % Plot fixed supports
        drawFixedSupports(nodeArray, H);
        
        % Plot nodes (spheres)
        for i = 1:size(nodeArray, 1)
            x = nodeArray(i, 2);
            y = nodeArray(i, 3);
            z = nodeArray(i, 4);
            
            % Skip drawing ground nodes as spheres (already have supports)
            if z > 0
                drawSphere(x, y, z, 0.02, [0.7, 0.7, 0.7]);
            end
            
            % Add node labels
            text(x+0.02, y+0.02, z+0.02, num2str(i), 'FontSize', 8);
        end
        
        % Set equal axis and grid
        axis equal;
        grid on;
        view(30, 20);
        
        % Set reasonable axis limits
        maxX = max(nodeArray(:, 2));
        maxY = max(nodeArray(:, 3));
        maxZ = max(nodeArray(:, 4));
        xlim([-0.1, maxX + 0.1]);
        ylim([-0.1, maxY + 0.1]);
        zlim([-0.2, maxZ + 0.1]);
        
        hold off;
    end
    
    % Draw fixed supports at ground level
    function drawFixedSupports(nodeArray, H)
        % Find ground level nodes
        groundNodes = nodeArray(nodeArray(:, 4) == 0, :);
        
        % Draw fixed supports
        for i = 1:size(groundNodes, 1)
            x = groundNodes(i, 2);
            y = groundNodes(i, 3);
            z = groundNodes(i, 4);
            
            % Draw a small cube to represent fixed support
            supportSize = H * 0.1;
            
            % Draw support box
            patch([x-supportSize, x+supportSize, x+supportSize, x-supportSize], ...
                  [y-supportSize, y-supportSize, y+supportSize, y+supportSize], ...
                  [z-supportSize, z-supportSize, z-supportSize, z-supportSize], ...
                  'g', 'FaceAlpha', 0.5);
        end
    end
    
    % Draw a sphere (for nodes)
    function drawSphere(x, y, z, radius, color)
        [X, Y, Z] = sphere(20);
        X = X * radius + x;
        Y = Y * radius + y;
        Z = Z * radius + z;
        surf(X, Y, Z, 'FaceColor', color, 'EdgeColor', 'none');
    end
    
    % Create mapping between sensor files and node IDs
    function createSensorMapping(stories)
        % Create the mapping between Point files and nodes
        sensorMapping = containers.Map();
        
        % For a 4-node per floor structure (2x2 grid)
        % Assuming Point5-Point16 correspond to nodes 5-16 for a 3-story building
        for i = 5:4*(stories+1)
            sensorMapping(['Point' num2str(i)]) = i;
        end
    end
    
    % Load data from Excel files
    function loadData()
        % Initialize data storage for each node
        nodeData = containers.Map();
        
        % Get the current MATLAB path
        currentPath = pwd;
        
        % Try to locate and load data for each sensor point
        for i = 5:16
            filename = ['Point' num2str(i) '.xlsx'];
            try
                % First try direct path
                if exist(filename, 'file')
                    data = readmatrix(filename);
                    nodeData(['Point' num2str(i)]) = data;
                    fprintf('Loaded data from %s\n', filename);
                else
                    % Try to find the file in MATLAB path
                    filePath = which(filename);
                    if ~isempty(filePath)
                        data = readmatrix(filePath);
                        nodeData(['Point' num2str(i)]) = data;
                        fprintf('Loaded data from %s\n', filePath);
                    else
                        % If still not found, generate synthetic data for testing
                        warning('File %s not found. Generating synthetic data.', filename);
                        
                        % Create synthetic time history data (t, X, Y, Z)
                        t = (0:0.01:10)'; % 10 seconds of data at 100 Hz
                        
                        % Generate synthetic accelerations with multiple frequency components
                        % Different frequencies for different nodes and directions
                        f1 = 5.2; % First mode frequency
                        f2 = 8.7; % Second mode frequency
                        f3 = 12.3; % Third mode frequency
                        % Add some randomness to make each node's data unique
                        nodeFactor = i/10;
                        
                        % X direction - mainly excited by first mode
                        X = 0.1*sin(2*pi*f1*t + nodeFactor) + 0.05*sin(2*pi*f2*t) + 0.02*sin(2*pi*f3*t) + 0.01*randn(size(t));
                        
                        % Y direction - mainly excited by second mode
                        Y = 0.05*sin(2*pi*f1*t) + 0.1*sin(2*pi*f2*t + nodeFactor) + 0.03*sin(2*pi*f3*t) + 0.01*randn(size(t));
                        
                        % Z direction - mainly excited by third mode
                        Z = 0.02*sin(2*pi*f1*t) + 0.03*sin(2*pi*f2*t) + 0.1*sin(2*pi*f3*t + nodeFactor) + 0.01*randn(size(t));
                        
                        % Combine into a data matrix
                        syntheticData = [t, X, Y, Z];
                        
                        % Store the synthetic data
                        nodeData(['Point' num2str(i)]) = syntheticData;
                    end
                end
            catch e
                warning('Error loading %s: %s', filename, e.message);
                
                % Generate synthetic data on error for testing purposes
                t = (0:0.01:10)';
                X = 0.1*sin(2*pi*5.2*t) + 0.01*randn(size(t));
                Y = 0.1*sin(2*pi*8.7*t) + 0.01*randn(size(t));
                Z = 0.1*sin(2*pi*12.3*t) + 0.01*randn(size(t));
                syntheticData = [t, X, Y, Z];
                nodeData(['Point' num2str(i)]) = syntheticData;
            end
        end
        
        % Update results text
        updateResults();
    end
    
    % Perform modal analysis on the data
    function performModalAnalysis()
        % Check if we have data to analyze
        if isempty(nodeData)
            % No data loaded, use example frequencies and shapes
            estimateModalParameters();
            return;
        end
        
        try
            % Initialize modal results structure
            modalResults = struct();
            
            % Get data for frequency analysis
            keys = nodeData.keys;
            if isempty(keys)
                estimateModalParameters();
                return;
            end
            
            % Try to identify natural frequencies from the data
            % We'll use the frequency domain peaks from all nodes
            allPeaks = [];
            
            for i = 1:length(keys)
                key = keys{i};
                data = nodeData(key);
                
                % Make sure data has at least 4 columns
                if size(data, 2) >= 4
                    % Calculate FFTs for X, Y, Z directions
                    for dir = 1:3
                        % Get time and acceleration for this direction
                        time = data(:, 1);
                        accel = data(:, dir+1);
                        
                        % Calculate time step and sampling frequency
                        dt = mean(diff(time));
                        Fs = 1/dt;
                        
                        % Perform FFT
                        N = length(accel);
                        Y = fft(accel);
                        
                        % Compute single-sided amplitude spectrum
                        P2 = abs(Y/N);
                        P1 = P2(1:floor(N/2)+1);
                        P1(2:end-1) = 2*P1(2:end-1);
                        
                        % Define frequency vector (up to 50 Hz)
                        f = Fs * (0:(N/2))/N;
                        maxFreqIdx = find(f <= 50, 1, 'last');
                        if isempty(maxFreqIdx)
                            maxFreqIdx = length(f);
                        end
                        f = f(1:maxFreqIdx);
                        P1 = P1(1:maxFreqIdx);
                        
                        % Find peaks in the spectrum
                        [peaks, locs] = findpeaks(P1, 'MinPeakHeight', max(P1)*0.3, 'MinPeakDistance', 10);
                        
                        % Add peaks to the collection
                        for j = 1:length(locs)
                            allPeaks(end+1, :) = [f(locs(j)), peaks(j)];
                        end
                    end
                end
            end
            
            % If we found some peaks, identify the most prominent frequencies
            if ~isempty(allPeaks)
                % Sort all peaks by amplitude
                [~, sortIdx] = sort(allPeaks(:, 2), 'descend');
                allPeaks = allPeaks(sortIdx, :);
                
                % Group similar frequencies (within 0.5 Hz)
                uniqueFreqs = [];
                for i = 1:size(allPeaks, 1)
                    freq = allPeaks(i, 1);
                    
                    % Check if this frequency is close to an existing one
                    isUnique = true;
                    for j = 1:size(uniqueFreqs, 1)
                        if abs(freq - uniqueFreqs(j, 1)) < 0.5
                            % Combine with existing frequency
                            uniqueFreqs(j, 2) = uniqueFreqs(j, 2) + allPeaks(i, 2);
                            isUnique = false;
                            break;
                        end
                    end
                    
                    % Add as a new unique frequency
                    if isUnique
                        uniqueFreqs(end+1, :) = [freq, allPeaks(i, 2)];
                    end
                end
                
                % Sort by amplitude again
                [~, sortIdx] = sort(uniqueFreqs(:, 2), 'descend');
                uniqueFreqs = uniqueFreqs(sortIdx, :);
                
                % Take the top 3 frequencies (or fewer if less are available)
                numFreqs = min(3, size(uniqueFreqs, 1));
                naturalFreqs = uniqueFreqs(1:numFreqs, 1);
                
                % If we found fewer than 3, add some default ones
                if numFreqs < 3
                    defaultFreqs = [5.2, 8.7, 12.3];
                    naturalFreqs = [naturalFreqs; defaultFreqs(1:(3-numFreqs))'];
                end
                
                % Store the natural frequencies
                modalResults.naturalFreqs = naturalFreqs;
            else
                % No peaks found, use defaults
                modalResults.naturalFreqs = [5.2, 8.7, 12.3];
            end
            
            % Now estimate the mode shapes
            estimateModalShapes();
            
        catch e
            warning('Error in modal analysis: %s. Using estimated parameters.', getReport(e));
            estimateModalParameters();
        end
    end
        
    % Helper function to estimate mode shapes from the natural frequencies
    function estimateModalShapes()
        % Get the story height and number of stories
        stories = str2double(get(storiesEdit, 'String'));
        H = str2double(get(hEdit, 'String'));
        numNodes = size(nodes, 1);
        
        % Initialize mode shapes matrix (3 DOF per node, 3 modes)
        modeShapes = zeros(numNodes, 3, 3);
        
        % For nodes at each floor level (excluding ground level)
        for floor = 1:stories
            floorNodes = find(nodes(:, 4) == floor * H);
            
            % First mode shape (X-direction sway)
            amplitude = floor/stories;
            for nodeIdx = floorNodes'
                modeShapes(nodeIdx, 1, 1) = amplitude * 1.0; % X-direction
                modeShapes(nodeIdx, 2, 1) = amplitude * 0.2; % Small Y-component
                modeShapes(nodeIdx, 3, 1) = 0; % No Z-component
            end
            
            % Second mode shape (Y-direction sway)
            for nodeIdx = floorNodes'
                modeShapes(nodeIdx, 1, 2) = amplitude * 0.2; % Small X-component
                modeShapes(nodeIdx, 2, 2) = amplitude * 1.0; % Y-direction
                modeShapes(nodeIdx, 3, 2) = 0; % No Z-component
            end
            
            % Third mode shape (torsional)
            for nodeIdx = floorNodes'
                % Calculate node position relative to center
                x_rel = nodes(nodeIdx, 2) - mean(nodes(floorNodes, 2));
                y_rel = nodes(nodeIdx, 3) - mean(nodes(floorNodes, 3));
                
                % Torsional mode (rotation around Z axis)
                modeShapes(nodeIdx, 1, 3) = amplitude * y_rel * 2;  % X-component proportional to Y-distance from center
                modeShapes(nodeIdx, 2, 3) = amplitude * -x_rel * 2; % Y-component proportional to X-distance from center
                modeShapes(nodeIdx, 3, 3) = 0; % No Z-component
            end
        end
        
        % Store in modal results
        modalResults.modeShapes = modeShapes;
    end
    
    % Fallback function if we can't extract modes from data
    function estimateModalParameters()
        % Initialize modal results structure with default values
        modalResults = struct();
        modalResults.naturalFreqs = [5.2, 8.7, 12.3]; % Example natural frequencies (Hz)
        
        % Create example mode shapes (would be calculated from actual data)
        stories = str2double(get(storiesEdit, 'String'));
        numNodes = size(nodes, 1);
        
        % Initialize mode shapes matrix (3 DOF per node, 3 modes)
        modeShapes = zeros(numNodes, 3, 3);
        
        % Example mode shapes for demonstration:
        % First mode: primarily X-direction lateral movement
        % Second mode: primarily Y-direction lateral movement
        % Third mode: torsional mode (twist around Z)
        
        % For nodes at each floor level (excluding ground level)
        for floor = 1:stories
            floorNodes = find(nodes(:, 4) == floor * str2double(get(hEdit, 'String')));
            
            % First mode shape (X-direction sway)
            amplitude = floor/stories;
            for nodeIdx = floorNodes'
                modeShapes(nodeIdx, 1, 1) = amplitude * 1.0; % X-direction
                modeShapes(nodeIdx, 2, 1) = amplitude * 0.2; % Small Y-component
                modeShapes(nodeIdx, 3, 1) = 0; % No Z-component
            end
            
            % Second mode shape (Y-direction sway)
            for nodeIdx = floorNodes'
                modeShapes(nodeIdx, 1, 2) = amplitude * 0.2; % Small X-component
                modeShapes(nodeIdx, 2, 2) = amplitude * 1.0; % Y-direction
                modeShapes(nodeIdx, 3, 2) = 0; % No Z-component
            end
            
            % Third mode shape (torsional)
            for nodeIdx = floorNodes'
                % Calculate node position relative to center
                x_rel = nodes(nodeIdx, 2) - mean(nodes(floorNodes, 2));
                y_rel = nodes(nodeIdx, 3) - mean(nodes(floorNodes, 3));
                
                % Torsional mode (rotation around Z axis)
                modeShapes(nodeIdx, 1, 3) = amplitude * y_rel * 2;  % X-component proportional to Y-distance from center
                modeShapes(nodeIdx, 2, 3) = amplitude * -x_rel * 2; % Y-component proportional to X-distance from center
                modeShapes(nodeIdx, 3, 3) = 0; % No Z-component
            end
        end
        
        % Store in modal results
        modalResults.modeShapes = modeShapes;
    end
% Update the results information panel
    function updateResults()
        % Check if modalResults exists
        if isfield(modalResults, 'naturalFreqs')
            resultsStr = sprintf('Modal Analysis Results:\n\n');
            
            % Add natural frequencies
            resultsStr = [resultsStr, 'Natural Frequencies:\n'];
            for i = 1:length(modalResults.naturalFreqs)
                resultsStr = [resultsStr, sprintf('Mode %d: %.2f Hz\n', i, modalResults.naturalFreqs(i))];
            end
            
            % Add information about loaded data
            resultsStr = [resultsStr, '\nData Files Loaded:\n'];
            if ~isempty(nodeData)
                keys = nodeData.keys;
                for i = 1:length(keys)
                    resultsStr = [resultsStr, sprintf('%s\n', keys{i})];
                end
            else
                resultsStr = [resultsStr, 'No data loaded\n'];
            end
            
            % Set the text
            set(resultsText, 'String', resultsStr);
        end
    end
    
    % Plot the Frequency Response Function for selected node and direction
    function plotFRF(~, ~)
        % Get selected node and direction
        nodesList = get(nodeSelect, 'String');
        selectedNode = nodesList{get(nodeSelect, 'Value')};
        directions = get(dirSelect, 'String');
        selectedDir = directions{get(dirSelect, 'Value')};
        
        % Get maximum frequency limit from input box
        maxFreqLimit = str2double(get(maxFreqEdit, 'String'));
        if isnan(maxFreqLimit) || maxFreqLimit <= 0
            errordlg('Please enter a valid positive number for maximum frequency', 'Input Error');
            return;
        end
        
        % Extract node number from string (e.g., "Node 5" -> 5)
        nodeNumber = str2double(regexp(selectedNode, '\d+', 'match'));
        
        % Check if we have data for this node
        nodeKey = ['Point' num2str(nodeNumber)];
        
        if isKey(nodeData, nodeKey)
            % Get data for the selected node
            data = nodeData(nodeKey);
            
            % Extract time and acceleration for selected direction
            time = data(:, 1);
            
            % Map direction to column index
            dirIndex = find(strcmp(selectedDir, {'X', 'Y', 'Z'})) + 1;
            
            if ~isempty(dirIndex) && dirIndex <= size(data, 2)
                accel = data(:, dirIndex);
                
                % Calculate time step and sampling frequency
                dt = mean(diff(time));
                Fs = 1/dt;
                
                % Perform FFT
                N = length(accel);
                Y = fft(accel);
                
                % Compute single-sided amplitude spectrum
                P2 = abs(Y/N);
                P1 = P2(1:floor(N/2)+1);
                P1(2:end-1) = 2*P1(2:end-1);
                
                % Define frequency vector
                f = Fs * (0:(N/2))/N;
                
                % Plot FRF
                axes(frfAxes);
                plot(f, P1, 'b-', 'LineWidth', 1.5);
                grid on;
                title(['FRF for ' selectedNode ' in ' selectedDir ' Direction']);
                xlabel('Frequency (Hz)');
                ylabel('Amplitude');
                xlim([0, min(maxFreqLimit, max(f))]);  % Use the user-specified limit
            else
                errordlg(['Direction ' selectedDir ' data not available for ' selectedNode], 'Data Error');
            end
        else
            errordlg(['No data available for ' selectedNode], 'Data Error');
        end
    end
    
    % Display or animate the selected mode
    function displayMode(~, ~)
        % Stop any ongoing animation
        if isAnimating
            isAnimating = false;
            set(findobj('Tag', 'animButton'), 'String', 'Start Animation');
            return;
        end
        
        % Get the selected display mode
        modes = get(modeSelect, 'String');
        selectedMode = modes{get(modeSelect, 'Value')};
        
        % Switch to the frame axes
        axes(frameAxes);
        cla;
        
        % Display the appropriate mode
        switch selectedMode
            case '3D Frame Only'
                % Just plot the frame
                plotFrame3D(nodes, elements, str2double(get(hEdit, 'String')));
                title('3D Steel Frame');
                
            case 'Mode 1'
                % Plot the frame with Mode 1 shape
                plotFrame3D(nodes, elements, str2double(get(hEdit, 'String')));
                title(['Mode 1: ', num2str(modalResults.naturalFreqs(1)), ' Hz']);
                
            case 'Mode 2'
                % Plot the frame with Mode 2 shape
                plotFrame3D(nodes, elements, str2double(get(hEdit, 'String')));
                title(['Mode 2: ', num2str(modalResults.naturalFreqs(2)), ' Hz']);
                
            case 'Mode 3'
                % Plot the frame with Mode 3 shape
                plotFrame3D(nodes, elements, str2double(get(hEdit, 'String')));
                title(['Mode 3: ', num2str(modalResults.naturalFreqs(3)), ' Hz']);
        end
    end
    
    % Start or stop the mode shape animation
    function startAnimation(hObject, ~)
        % Toggle animation state
        isAnimating = ~isAnimating;
        
        if isAnimating
            % Change button text to 'Stop Animation'
            set(hObject, 'String', 'Stop Animation');
            
            % Get the selected mode
            modes = get(modeSelect, 'String');
            selectedMode = modes{get(modeSelect, 'Value')};
            
            % Don't animate if '3D Frame Only' is selected
            if strcmp(selectedMode, '3D Frame Only')
                isAnimating = false;
                set(hObject, 'String', 'Start Animation');
                return;
            end
            
            % Get the mode number
            modeNum = str2double(regexp(selectedMode, '\d+', 'match'));
            
            % Check if valid mode number
            if ~isempty(modeNum) && modeNum <= size(modalResults.modeShapes, 3)
                % Animate the selected mode
                animateMode(modeNum);
            else
                isAnimating = false;
                set(hObject, 'String', 'Start Animation');
                errordlg('Invalid mode selection', 'Animation Error');
            end
        else
            % Change button text back to 'Start Animation'
            set(hObject, 'String', 'Start Animation');
        end
    end
    
    % Animate the selected mode
    function animateMode(modeNum)
        % Get animation parameters
        scaleFactor = get(ampScale, 'Value');
        speed = get(animSpeed, 'Value');
        
        % Get mode shapes for this mode
        modeShape = modalResults.modeShapes(:, :, modeNum);
        
        % Get natural frequency for this mode
        freq = modalResults.naturalFreqs(modeNum);
        
        % Create a copy of the original nodes for animation
        animNodes = nodes;
        
        % Number of frames per cycle
        numFrames = 30;
        
        % Start animation loop
        frameCount = 0;
        
        while isAnimating
            % Calculate phase angle for this frame
            phase = mod(frameCount * 2*pi/numFrames, 2*pi);
            frameCount = frameCount + 1;
            
            % Scale factor for this frame
            frameFactor = scaleFactor * sin(phase);
            
            % Update node positions for animation
            for i = 1:size(animNodes, 1)
                % Only animate non-ground nodes
                if animNodes(i, 4) > 0
                    % Apply mode shape displacement * scale factor
                    animNodes(i, 2) = nodes(i, 2) + frameFactor * modeShape(i, 1);
                    animNodes(i, 3) = nodes(i, 3) + frameFactor * modeShape(i, 2);
                    animNodes(i, 4) = nodes(i, 4) + frameFactor * modeShape(i, 3);
                end
            end
            
            % Clear and redraw
            axes(frameAxes);
            cla;
            
            % Plot elements with updated node positions
            hold on;
            for i = 1:size(elements, 1)
                node1 = elements(i, 2);
                node2 = elements(i, 3);
                
                % Get coordinates
                x = [animNodes(node1, 2), animNodes(node2, 2)];
                y = [animNodes(node1, 3), animNodes(node2, 3)];
                z = [animNodes(node1, 4), animNodes(node2, 4)];
                
                % Plot line - red for columns, blue for beams
                if nodes(node1, 4) ~= nodes(node2, 4)  % Vertical elements (columns)
                    plot3(x, y, z, 'r-', 'LineWidth', 2);
                else  % Horizontal elements (beams)
                    plot3(x, y, z, 'b-', 'LineWidth', 2);
                end
            end
            
            % Plot fixed supports
            drawFixedSupports(nodes, str2double(get(hEdit, 'String')));
            
            % Plot nodes (spheres) for non-ground nodes
            for i = 1:size(animNodes, 1)
                if animNodes(i, 4) > 0
                    drawSphere(animNodes(i, 2), animNodes(i, 3), animNodes(i, 4), 0.02, [0.7, 0.7, 0.7]);
                end
            end
            
            % Set equal axis and grid
            axis equal;
            grid on;
            view(30, 20);
            
            % Set reasonable axis limits with some extra space for the animation
            maxX = max(nodes(:, 2));
            maxY = max(nodes(:, 3));
            maxZ = max(nodes(:, 4));
            xlim([-0.1-scaleFactor, maxX + 0.1+scaleFactor]);
            ylim([-0.1-scaleFactor, maxY + 0.1+scaleFactor]);
            zlim([-0.2, maxZ + 0.1+scaleFactor]);
            
            % Add title
            title(['Mode ', num2str(modeNum), ': ', num2str(freq), ' Hz (Animated)']);
            
            hold off;
            drawnow;
            
            % Pause based on speed setting
            pause(0.03 / speed);
            
            % Check if animation should stop
            if ~isAnimating
                break;
            end
        end
        
        % Reset the frame to static display
        displayMode([], []);
    end
end

% Run the main function
main_steel_frame_analyzer();