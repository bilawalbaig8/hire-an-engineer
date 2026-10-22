# Desktop apps, plugins and editors

When to read this: the system is a desktop program, a tool with an extension or plugin system, an editor, or a web-technology app packaged for the desktop. Sources in this field are mostly unverified; where a claim is general practice it says so.

## Decisions that matter most

| Decision | Choose X when | Otherwise Y | What you give up |
|---|---|---|---|
| Technology | **A web view wrapped in a desktop shell** (Electron or Tauri style) when your team already knows web technology and the app is mostly screens. | **A native toolkit** when you need the best performance, small size, deep system integration, or a long-lived tool. (general practice; unverified sources S-DESK-1, S-DESK-2, S-DESK-4 describe the main options) | Web shells give up size and memory (Electron) or maturity (newer shells). Native gives up reuse of web skills and code. |
| Process layout | **Split the program in two worlds**: a privileged side that touches files, network and the system, and a restricted screen side that only draws and asks the privileged side through a narrow, checked channel. (unverified source S-DESK-1 describes this for Electron) | A single process only for tiny, trusted tools. | Two worlds give up some simplicity for a much smaller security risk. |
| Plugins | **Run plugins outside the main program** (in separate processes), give them a small, versioned API and explicit permissions. (unverified source S-DESK-3 describes this for a well-known editor) | In-process plugins only when speed demands it and plugins come from trusted authors. | Out-of-process plugins give up some speed and convenience; they protect the host from crashes and abuse. |
| UI structure | **Separate what the screen shows from the logic**, using one of the established presentation patterns (model-view-controller, model-view-presenter, presentation model). (unverified source S-DESK-5 compares them) | Keep it inline only in throwaway tools. | The separation gives up a little speed of first development for testability. |
| Data and settings | **Store user data in the platform's standard per-user folders**, in an open or documented format, with a version number inside. | A database file when queries or size demand it. | Standard folders give up total control of layout; documented formats give up the freedom to change them casually. |
| Updates | **Automatic updates with signing**, so users get fixes and can trust what they install. | Manual updates for closed enterprise environments. | Auto-update gives up some control and needs a signing and release process. |
| Offline and sync | **Treat the desktop as local-first**: the app works without a network and syncs when it can (see `mobile` for the sync rule discussion). | Online-only when the product is a window onto a service. | Local-first gives up simple "always fresh". |

## Typical shapes

- **Single-user local tool:** one program, files or an embedded database, an update mechanism.
- **Editor or tool with plugins:** a small core, a plugin host in separate processes, a versioned API, a permission prompt for each plugin.
- **Web shell app:** a privileged main process, restricted screen processes, a narrow bridge between them.
- **Cloud-connected desktop client:** local cache and queue, background sync, token in the system's secure store.

## Failure modes

- **A screen process with full system access:** one injected script can read files or run programs.
- **Plugins that can crash or freeze the host**, or read anything.
- **Slow start and high memory use** from loading everything at launch.
- **User data trapped in a private format** with no export or backup path.
- **Updates that cannot be rolled back**, or unsigned updates.
- **Works only on the developer's operating system:** paths, line endings, permissions and installers differ per platform.

## Questions that change the design

- Which operating systems must be supported? Is installation by non-administrators required?
- Will third parties write plugins? How much do you trust them?
- Does the app touch files, devices or the network in ways that need permissions?
- Must it work offline? Does it sync to a server?
- How will users receive updates, and who signs the releases?

## Checks before you hand it back

- [ ] The privileged and restricted parts are named, and the channel between them is narrow and checked.
- [ ] If there are plugins: they run outside the main program, with a versioned API and permissions.
- [ ] User data sits in the standard per-user location in a documented, versioned format, with an export.
- [ ] An update path exists with signing, and a way back if an update fails.
- [ ] The app was tried on every supported operating system, including paths with spaces and non-English characters.
- [ ] Startup time and memory have budgets and a way to measure them.

## Sources
Unverified leads only (pages reachable but not read in full): S-DESK-1, S-DESK-2, S-DESK-3, S-DESK-4, S-DESK-5
