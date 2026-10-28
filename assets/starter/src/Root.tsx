import {Composition} from 'remotion';
import {ThemeFilm,project} from './Film';
export const Root=()=> <Composition id="ThemeVideo" component={ThemeFilm} width={project.width} height={project.height} fps={project.fps} durationInFrames={project.durationFrames}/>;
